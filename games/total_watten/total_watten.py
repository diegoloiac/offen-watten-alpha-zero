import numpy as np
from EnvironmentSelector import EnvironmentSelector
from games.watten_sub_game.WattenSubGame import WattenSubGame

from loggers import stdout_logger

# allowed moves:
# 0 -> make the best sub_watten choice (rank, suit or play card)
moves = {"make_best_move": 0,
         "raise_points": 1,
         "fold_hand": 2,
         "accept_raise": 3,
         "fold_hand_and_show_valid_raise": 4}  # can raise in last hand but some conditions should be verified
rank_names = {0: "7", 1: "8", 2: "9", 3: "10", 4: "unter", 5: "ober", 6: "kinig", 7: "ass", 8: "weli", None: "-"}
# suit_names = {0: "♠︎", 1: "♥", 2: "♣︎", 3: "∙"}
suit_names = {0: "laab♠", 1: "herz♥", 2: "oachl♣", 3: "schell∙", None: "-"}


# returns the unique id of a card given its rank and suit
def get_id(rank, suit):
    if rank > 8 or suit > 3:
        raise CardParsingError('Max rank is 8 (got {}) and max suit is 3 (got {})'.format(rank, suit))
    if rank == 8:  # 8 can only be the weli and the unique id is 8
        return 32
    return suit * 8 + rank


def get_rs(id_):
    if id_ > 32:
        raise CardParsingError('Card id is between 1 and 32 (got {})'.format(id_))
    if id_ == 32:
        return 8, 3
    s = np.floor(id_ / 8)
    r = id_ - 8 * s
    return int(r), int(s)


def human_readable_card(card_id):
    r, s = get_rs(card_id)
    if r == 8:
        return rank_names[8]
    else:
        return '{} of {}'.format(rank_names[r], suit_names[s])


# rules:
# first pick a rank (from 7, 8, 9...)
# other player pick a suit (laab, herz...)
# first plays a card
# second plays a card
# ....
# repeat until one player wins 3 hands


# Schlagtausch e Bessere are not implemented in the current version of the game
# noinspection PyAttributeOutsideInit
class WorldTotalWatten(object):

    def __init__(self, logger=stdout_logger):
        self.LOG = logger
        self.refresh()

    def refresh(self):
        # getting agent for sub_watten
        self.env_selector = EnvironmentSelector()
        self.agent = self.env_selector.get_agent("sub_watten_agent_train_default")
        self.agent.set_exploration_enabled(False)

        # loading best model for sub_watten agent
        self.agent.load("../../watten_sub_game/training/gen3/best.h5")

        # create a sub_watten game
        self.sub_watten_game = WattenSubGame()

        # player can be either 1 or -1
        # player 1 is A
        # player -1 is B
        self.current_player = 1

        # player who distributes cards when the game starts; each game the starting player is switched
        # the opponent picks rank and playes the first move
        self.distributing_cards_player = -1

        # overall score of the game
        self.player_A_score = 0
        self.player_B_score = 0

        # points to achieve for winning a game
        self.win_threshold = 15

        self._refresh_state_single_hand()

        # player who won the game
        self.winning_player = None

        self.moves = moves

        # list of actions taken in a game, used for debugging purposes
        self.moves_series = []
        self.starting_state = f"\n{self.current_player}, {self.distributing_cards_player}, {self.player_A_score}, {self.player_B_score}, {self.player_A_hand}, {self.player_B_hand}, {self.played_cards}, {self.current_game_player_A_score}, {self.current_game_player_B_score}, {self.current_game_prize}, {self.is_last_move_raise}, {self.is_last_move_accepted_raise}, {self.is_last_hand_raise_valid}, {self.first_card_deck}, {self.last_card_deck}, {self.rank}, {self.suit}"

    def _refresh_state_single_hand(self):
        # init deck
        self.deck = list(range(33))
        np.random.shuffle(self.deck)

        # init starting hands
        self.player_A_hand = []
        self.player_B_hand = []

        # give cards to players
        self.player_A_hand += self.deck[-5:]
        self.deck = self.deck[:-5]
        self.player_B_hand += self.deck[-5:]
        self.deck = self.deck[:-5]

        # init board
        self.played_cards = []

        # init player scores, needs 3 for winning the hand
        # do not confuse those two fields with the total score achieved
        self.current_game_player_A_score = 0
        self.current_game_player_B_score = 0

        # is True only if the last move was a raise
        self.is_last_move_raise = False
        self.is_last_move_accepted_raise = False

        # raise in last hand implies some specific rules. see act method
        self.is_last_hand_raise_valid = None

        # first and last card in deck (doesn't really matter where those cards are taken :D )
        self.first_card_deck = self.deck[-1:][0]
        self.deck = self.deck[:-1]
        self.last_card_deck = self.deck[-1:][0]
        self.deck = self.deck[:-1]

        self.rank = None  # schlag
        self.suit = None  # farb

        self._set_initial_game_prize()

        for card in self.player_A_hand:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)
        for card in self.player_B_hand:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)

    def _set_initial_game_prize(self):
        if (self.win_threshold - self.player_A_score) <= 2:
            if self.player_B_score < 10:
                self.current_game_prize = 4
            else:
                self.current_game_prize = 3
            return
        if (self.win_threshold - self.player_B_score) <= 2:
            if self.player_A_score < 10:
                self.current_game_prize = 4
            else:
                self.current_game_prize = 3
            return

        self.current_game_prize = 2

    def get_valid_moves_zeros(self):
        valid_moves = self.get_valid_moves()
        if len(valid_moves) == 0:
            self.display()
            raise ValidMovesError("Valid moves cannot be 0!")
        valid_moves_zeros = [0] * 5  # number of possible moves
        for valid_move in valid_moves:
            valid_moves_zeros[valid_move] = 1
        return valid_moves_zeros

    def get_valid_moves(self):
        """

        :rtype: list
        """

        # a player can raise at any time
        # if the last move was a raise then the player can fold or accept it
        if self.is_last_move_raise and not self.is_last_move_accepted_raise:
            valid_moves = [moves["fold_hand"], moves["accept_raise"]]
            if self.is_last_hand_raise_valid is not None:
                valid_moves.append(moves["fold_hand_and_show_valid_raise"])
            self.LOG.debug(f"Valid moves for player [{self.current_player}] are {valid_moves}")
            return valid_moves

        # if last move was not a raise, then the player can make the best sub_watten move
        valid_moves = [moves["make_best_move"]]

        if (not self.is_last_move_raise) and (not self.is_last_move_accepted_raise) and\
                (self.is_last_hand_raise_valid is None) and self.check_allowed_raise_situation():
            valid_moves.append(self.moves["raise_points"])

        self.LOG.debug(f"Valid moves for player [{self.current_player}] are {valid_moves}")
        return valid_moves

    def check_allowed_raise_situation(self):
        # it makes sense to raise only if a player can't win the game with the current game prize
        if self.current_player == 1 and (self.player_A_score + self.current_game_prize) < self.win_threshold:
            return True
        if self.current_player == -1 and (self.player_B_score + self.current_game_prize) < self.win_threshold:
            return True
        return False

    # make a single move and apply changes to inner state of the world
    # modify the current state of the game and returns an outcome
    # the function should return 2 values: the outcome of the move and the next player
    # the outcome should be wither
    # - end, a single game is ended because one of the 2 players won 3 hands or a player folds
    # - continue, a player made a move that didn't bring the current game to an end
    # - current_player_won
    # the next player can be either 1 or -1
    def act(self, action):
        num_played_cards = len(self.played_cards)
        if action not in self.get_valid_moves():
            raise InvalidActionError("Action %d cannot be played" % action)

        if action > 4:
            raise InvalidActionError("Action %d is not valid" % action)
        if self.current_game_player_A_score > 3 or self.current_game_player_B_score > 3:
            raise InconsistentStateError("Current game score cannot exceed 3. Player 1 [%d] and player -1 [%d]"
                                         % (self.current_game_player_A_score, self.current_game_player_B_score))

        self.moves_series.append(action)

        if action == moves["raise_points"]:
            if self.is_last_move_raise or self.is_last_move_accepted_raise or self.is_last_hand_raise_valid is not None:
                raise InvalidActionError("Cannot raise if the previous move was a raise")
            self.LOG.debug(f"{self.current_player} raised points")
            self.is_last_move_raise = True
            if num_played_cards >= 8:
                self.is_last_hand_raise_valid = self._last_hand_raise_valid()
            self.current_game_prize += 1
            return self._act_continue_move()

        if action == moves["accept_raise"]:
            if self.is_last_move_raise is False or self.is_last_move_accepted_raise:
                raise InvalidActionError("Cannot accept raise if the previous move was not a raise")
            self.LOG.debug(f"{self.current_player} accepted raise")
            self.is_last_move_accepted_raise = True
            self.is_last_move_raise = False
            return self._act_continue_move()

        # if a player folds, then the prize is given to the opponent
        if action == moves["fold_hand"] or action == moves["fold_hand_and_show_valid_raise"]:
            if self.is_last_move_raise is False or self.is_last_move_accepted_raise:
                raise InvalidActionError("Cannot fold hand if the previous move was not a raise")
            self.LOG.debug(f"{self.current_player} folds hand")
            self._assign_points_fold()
            self._assign_winning_player()
            self.current_player = self.distributing_cards_player
            self.distributing_cards_player = self.distributing_cards_player * -1
            self._refresh_state_single_hand()
            return "end", self.current_player

        # if an action is not a raise, an accept raise or a fold, then the next move is definitely going to
        # reset the chance for raising
        self.is_last_move_accepted_raise = False
        self.is_last_move_raise = False

        # if an action is make best move, then the sub_watten agent will predict the move
        if action == moves["make_best_move"]:
            if self.is_last_move_raise:
                raise InvalidActionError("Cannot play a card if the previous move was a raise")

            self.LOG.debug(f"{self.current_player} made best sub_watten move")

            # set sub_watten game to represent the current state
            self.sub_watten_game.trueboard.init_world_to_state(self.current_player, self.distributing_cards_player,
                                                               self.player_A_hand, self.player_B_hand, self.played_cards,
                                                               self.current_game_player_A_score,
                                                               self.current_game_player_B_score, self.first_card_deck,
                                                               self.last_card_deck, self.rank, self.suit)

            best_move_array, v = self.agent.predict(self.sub_watten_game, self.sub_watten_game.get_cur_player())

            # index of the move in sub_watten
            move = np.argmax(best_move_array)

            # rank is between 33 and 42
            if 33 <= move < 42:
                self.rank = move % 33
                self.LOG.debug(f"{self.current_player} picked rank [{self.rank}]")
                return self._act_continue_move()

            # suit is between 42 and 46
            if 42 <= move < 46:
                self.suit = move % 42
                self.LOG.debug(f"{self.current_player} picked suit [{self.suit}]")
                return self._act_continue_move()

            if 0 <= move < 33:
                hand = self._get_current_player_hand()
                if move not in hand:
                    self.display()
                    raise InconsistentStateError(
                        'Played card [%d] not in %s of player %d' % (move, hand, self.current_player))

                self.LOG.debug(f"{self.current_player} played card {move}")

                self._remove_card_from_hand(move, self.current_player)

                if num_played_cards % 2 == 0:
                    if self.is_last_hand_raise_valid is not None and not self.is_last_hand_raise_valid:
                        # played cards are 8 and current player also raised without respecting the conditions
                        if self.current_player == 1:
                            self.player_B_score += self.current_game_prize
                        else:
                            self.player_A_score += self.current_game_prize
                        return self._hand_is_done_after_card_is_played_common()
                    self.played_cards.append(move)
                    return self._act_continue_move()
                else:
                    if self.is_last_hand_raise_valid is not None and not self.is_last_hand_raise_valid:
                        # played cards are 9 and current player also raised without respecting the conditions
                        if self.current_player == 1:
                            self.player_B_score += self.current_game_prize
                        else:
                            self.player_A_score += self.current_game_prize
                        return self._hand_is_done_after_card_is_played_common()

                    last_played_card = self._get_last_played_card()
                    self.played_cards.append(action)
                    current_played_card = action
                    current_player_wins = not self.compare_cards(last_played_card, current_played_card)
                    next_player_move = self._assign_points_move(current_player_wins)

                    if self.current_game_player_A_score == 3 or self.current_game_player_B_score == 3:
                        if self.current_game_player_A_score == 3:
                            self.player_A_score += self.current_game_prize
                        else:
                            self.player_B_score += self.current_game_prize
                        return self._hand_is_done_after_card_is_played_common()

                    self.current_player = next_player_move
                    return "continue", next_player_move

            raise InconsistentStateError("Best_move %d is not allowed." % move)

        self.display()
        raise InconsistentStateError("Action %d is not allowed." % action)

    def _hand_is_done_after_card_is_played_common(self):
        self._assign_winning_player()
        self.current_player = self.distributing_cards_player
        self.distributing_cards_player = self.distributing_cards_player * -1
        self._refresh_state_single_hand()
        return "end", self.current_player

    def _act_continue_move(self):
        self.current_player = self.current_player * -1
        return "continue", self.current_player

    def _assign_winning_player(self):
        if self.player_A_score >= self.win_threshold:
            self.winning_player = 1
        elif self.player_B_score >= self.win_threshold:
            self.winning_player = -1

    def _remove_card_from_hand(self, action, player):
        if player == 1:
            self.player_A_hand.remove(action)
            return
        if player == -1:
            self.player_B_hand.remove(action)
            return
        raise InvalidActionError("Player should be either 1 or -1. Got %d" % player)

    # if a player folds, then the prize is given to the opponent except when the raise was done in a not valid situation
    def _assign_points_fold(self):
        fold_points = self.current_game_prize - 1
        if self.is_last_hand_raise_valid is None or self.is_last_hand_raise_valid:
            if self.current_player == 1:
                self.player_B_score += fold_points
            if self.current_player == -1:
                self.player_A_score += fold_points
        else:
            if self.current_player == 1:
                self.player_A_score += fold_points
            if self.current_player == -1:
                self.player_B_score += fold_points

    # returns true if the player who raised the current turn satisfies the following rules:
    # - he has a trumpf
    # - his card has the same suit of the one played by the previous player
    # - his card wins against the one played by the opponent player
    def _last_hand_raise_valid(self):
        num_played_cards = len(self.played_cards)

        if num_played_cards not in (8, 9):
            raise InconsistentStateError("Num played cards when fold occurs in last hand can be either 8 or 9. Got %d." % num_played_cards)

        hidden_card = self._get_current_player_hand()[0]
        hidd_r, hidd_s = get_rs(hidden_card)

        if self.is_trumpf(hidd_r, hidd_s):
            return True
        if num_played_cards == 9:
            last_played_card = self._get_last_played_card()
            last_played_card_rank, last_played_card_suit = get_rs(last_played_card)

            if hidd_s == last_played_card_suit or not self.compare_cards(last_played_card, hidden_card):
                return True

        return False

    # after two cards have been compared, assign points and returns the player that should play the next move
    def _assign_points_move(self, current_player_wins):
        if current_player_wins:
            if self.current_player == 1:
                self.current_game_player_A_score += 1
                return 1
            else:
                self.current_game_player_B_score += 1
                return -1
        else:
            if self.current_player == 1:
                self.current_game_player_B_score += 1
                return -1
            else:
                self.current_game_player_A_score += 1
                return 1

    # routine for deciding whether a card (card1) wins over another card (card2)
    # returns true if the first card wins, false otherwise
    # the first card is expected to be played before the second one
    #
    # ORDER OF IMPORTANCE:
    # - Rechte (card with the same suit and rank chosen when the game started)
    # - Blinden (cards with the same rank of the chosen rank)
    # - Trümpfe (cards with the same suit of the chosen suit)
    # - Other cards (importance given by the rank)
    def compare_cards(self, card1, card2):

        card1_rank, card1_suit = get_rs(card1)
        card2_rank, card2_suit = get_rs(card2)

        #######################################################
        # RECHTE
        #######################################################

        # rechte is the strongest card
        if self.is_rechte(card1_rank, card1_suit):
            return True
        if self.is_rechte(card2_rank, card2_suit):
            return False

        #######################################################
        # BLINDEN
        #######################################################

        # the second strongest cards after the rechte are the blinde
        if self.is_blinde(card1_rank):
            return True
        if self.is_blinde(card2_rank):
            return False

        #######################################################
        # TRÜMPFEN
        #######################################################

        # if a played card has the same chosen suit, then the opponent for winning the hand should play
        # a card of the same suit but with higher rank
        if self.is_trumpf(card1_rank, card1_suit):
            if self.is_trumpf(card2_rank, card2_suit):
                # when both cards are trümpfe then wins the card with the highest rank
                return self.is_rank_higher(card1_rank, card2_rank)
            # a card of the chosen suit wins against a card without the chosen suit
            else:
                return True

        # if the first card is not trümpfe and the second is trümpfe, then the second card wins
        if self.suit == card2_suit:
            return False

        #######################################################
        # OTHER CARDS
        #######################################################

        # at this point if the second card has a different suit from the first card, then the first wins
        if card1_suit != card2_suit:
            return True

        # if the first and the second card are not trümpfe and have the same suit,
        # then the card with the highest rank wins
        return self.is_rank_higher(card1_rank, card2_rank)

    def is_rechte(self, card_rank, card_suit):
        if (self.rank == 8 and card_rank == 8) or (card_rank == self.rank and card_suit == self.suit):
            return True
        return False

    def is_blinde(self, card_rank):
        if card_rank == self.rank:
            return True
        return False

    def is_trumpf(self, card_rank, card_suit):
        if self.is_rechte(card_rank, card_suit):
            return False
        if self.suit == card_suit:
            return True

    def is_rank_higher(self, card1_rank, card2_rank):
        # the weli has the lowest rank
        if card1_rank == 8:
            return False
        # the weli has the lowest rank
        if card2_rank == 8:
            return True
        return card1_rank > card2_rank

    def is_game_end(self):
        if self.player_A_score >= self.win_threshold or self.player_B_score >= self.win_threshold:
            return True
        else:
            return False

    # this is called after act, player is the next player
    def is_won(self, player):
        if player not in [1, -1]:
            raise InvalidInputError("Player should be either 1 or -1. Input is %d." % player)

        if self.player_A_score >= self.win_threshold and self.player_B_score >= self.win_threshold:
            raise InconsistentStateError("Both player cannot exceed score threshold. Only one winner is allowed.")
        if player == -1 and self.player_A_score >= self.win_threshold:
            return True
        if player == 1 and self.player_B_score >= self.win_threshold:
            return True
        return False

    def get_player(self):
        return self.current_player

    # should return a unique id with the state of the game
    # the needed info are:
    # - observation value of current sub_watten state (101)
    # - points current hand current player (max 2)
    # - points current hand opponent player (max 2)
    # - points game current player (max 14)
    # - points game opponent player (max 14)
    # - last move raise (1)
    # - last move accepted raise (1)
    # - last hand raise valid (1)
    # - current prize (13)
    def observe(self, player):
        if player not in [1, -1]:
            raise InvalidInputError("Player should be either 1 or -1. Input is %d." % player)

        observation = np.zeros((149,))

        # set sub_watten game to current state
        self.sub_watten_game.trueboard.init_world_to_state(self.current_player, self.distributing_cards_player,
                                                           self.player_A_hand, self.player_B_hand, self.played_cards,
                                                           self.current_game_player_A_score,
                                                           self.current_game_player_B_score, self.first_card_deck,
                                                           self.last_card_deck, self.rank, self.suit)

        # observation value of sub_watten state
        best_move_array, v = self.agent.predict(self.sub_watten_game, self.sub_watten_game.get_cur_player())
        arg = np.rint(v*100).astype(int)
        observation[arg] = 1

        # points current hand current player
        index = 101  # 101
        points_current_hand_current = self.current_game_player_A_score if player == 1 else self.current_game_player_B_score
        if points_current_hand_current != 0:
            observation[index + points_current_hand_current - 1] = 1

        # points current hand opponent player
        index += 2  # 103
        points_current_hand_opponent = self.current_game_player_B_score if player == 1 else self.current_game_player_A_score
        if points_current_hand_opponent != 0:
            observation[index + points_current_hand_opponent - 1] = 1

        # points game current player
        index += 2  # 105
        points_game_current = self.player_A_score if player == 1 else self.player_B_score
        if points_game_current != 0:
            observation[index + points_game_current - 1] = 1

        # points game opponent player
        index += 14  # 119
        points_game_opponent = self.player_B_score if player == 1 else self.player_A_score
        if points_game_opponent != 0:
            observation[index + points_game_opponent - 1] = 1

        index += 14  # 133
        if self.is_last_move_raise:
            observation[index] = 1

        index += 1  # 134
        if self.is_last_move_accepted_raise:
            observation[index] = 1

        index += 1  # 135
        if self.is_last_hand_raise_valid is None:
            observation[index] = 0
        else:
            observation[index] = 1

        index += 1  # 136
        if self.current_game_prize - 3 >= 0:
            observation[index + self.current_game_prize - 3] = 1

        # total size = 136 + 13 = 149

        observation = observation.reshape((149, 1))
        return observation

    # def observation_str_raw(self, observe):
    #     new_observe = np.concatenate((observe, np.array([[1 if self.current_player == 1 else 0]])))
    #     print(new_observe)

    def _get_last_played_card(self):
        num_played_cards = len(self.played_cards)
        if num_played_cards == 0:
            return None
        return self.played_cards[num_played_cards - 1]

    def _get_opponent_hand(self):
        return self.player_B_hand if self.current_player == 1 else self.player_A_hand

    def _get_current_player_hand(self):
        return self.player_A_hand if self.current_player == 1 else self.player_B_hand

    def display(self):
        str_raise = ""
        if self.is_last_move_raise:
            str_raise = "- RAISE"
        if self.is_last_move_accepted_raise:
            str_raise = "- ACCEPTED RAISE"

        self.LOG.info(f"--- State of the game ---\nCurrent player: |{self.current_player}| "
                      f"and current game prize |{self.current_game_prize}| {str_raise}"
                      f"\nPlayer 1 points: |{self.player_A_score}| - Player -1 points: |{self.player_B_score}|"
                      f"\nPlayer 1 current: |{self.current_game_player_A_score}| - "
                      f"Player  -1 current: |{self.current_game_player_B_score}|"
                      f"\nPlayer  1 hand: {self._str_cards(self.player_A_hand)} - {self.player_A_hand}"
                      f"\nPlayer -1 hand: {self._str_cards(self.player_B_hand)} - {self.player_B_hand}"
                      f"\nRank: |{self.rank} - {rank_names[self.rank]}|, Suit: |{self.suit} - {suit_names[self.suit]}|"
                      f"\nPlayed cards: {self._str_cards(self.played_cards)}"
                      f"\n{self.distributing_cards_player}, {self.is_last_hand_raise_valid}, {self.first_card_deck}, {self.last_card_deck}")

        self.LOG.info(f"{self.starting_state}")
        self.LOG.info(f"{self.moves_series}")

    def _str_cards(self, cards):
        str_cards = ""
        for idx, card in enumerate(cards):
            str_cards += human_readable_card(card)
            str_cards += ' ({})'.format(card)
            if idx != len(cards) - 1:
                str_cards += ", "
        return str_cards

    def deepcopy(self):
        new_world = WorldTotalWatten()
        new_world.LOG = self.LOG
        new_world.current_player = self.current_player
        new_world.distributing_cards_player = self.distributing_cards_player
        new_world.deck = self.deck.copy()
        new_world.player_A_hand = self.player_A_hand.copy()
        new_world.player_B_hand = self.player_B_hand.copy()
        new_world.played_cards = self.played_cards.copy()
        new_world.player_A_score = self.player_A_score
        new_world.player_B_score = self.player_B_score
        new_world.current_game_player_A_score = self.current_game_player_A_score
        new_world.current_game_player_B_score = self.current_game_player_B_score
        new_world.current_game_prize = self.current_game_prize
        new_world.is_last_move_raise = self.is_last_move_raise
        new_world.is_last_move_accepted_raise = self.is_last_move_accepted_raise
        new_world.win_threshold = self.win_threshold
        new_world.first_card_deck = self.first_card_deck
        new_world.last_card_deck = self.last_card_deck
        new_world.rank = self.rank
        new_world.suit = self.suit
        new_world.is_last_hand_raise_valid = self.is_last_hand_raise_valid
        new_world.winning_player = self.winning_player

        new_world.starting_state = self.starting_state
        new_world.moves_series = self.moves_series.copy()
        return new_world

    def init_world_to_state(self, current_player, distributing_cards_player, player_A_score, player_B_score,
                            player_A_hand, player_B_hand, played_cards, current_game_player_A_score,
                            current_game_player_B_score, current_game_prize, is_last_move_raise,
                            is_last_move_accepted_raise, is_last_hand_raise_valid, first_card_deck, last_card_deck, rank, suit):

        self.current_player = current_player
        self.distributing_cards_player = distributing_cards_player
        self.player_A_score = player_A_score
        self.player_B_score = player_B_score
        self.player_A_hand = player_A_hand
        self.player_B_hand = player_B_hand
        self.played_cards = played_cards
        self.current_game_player_A_score = current_game_player_A_score
        self.current_game_player_B_score = current_game_player_B_score
        self.current_game_prize = current_game_prize
        self.is_last_move_raise = is_last_move_raise
        self.is_last_move_accepted_raise = is_last_move_accepted_raise
        self.is_last_hand_raise_valid = is_last_hand_raise_valid
        self.first_card_deck = first_card_deck
        self.last_card_deck = last_card_deck
        self.rank = rank
        self.suit = suit



class Error(Exception):
    """Base class for other exceptions"""
    pass


class InconsistentStateError(Error):
    """Raised when the state of the game is not consistent"""
    pass


class CardParsingError(Error):
    """Raised when there is a mistake in parsing card id to suit/rank and vice versa"""
    pass


class InvalidActionError(Error):
    """Raised when a taken action is not valid"""
    pass


class ValidMovesError(Error):
    """Raised when there there is an error related to the valid moves subroutine"""
    pass


class InvalidInputError(Error):
    """Raised when the input of a method is not legal. Validation error."""
    pass


if __name__ is "__main__":
    world = WorldTotalWatten()
