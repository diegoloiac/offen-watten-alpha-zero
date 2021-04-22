import numpy as np
import logging

# allowed moves:
# 0 - 32 -> play a card
# 33 - 41 -> pick rank, 41 is the weli
# 42 - 45 -> pick a suit
moves = {"play_card": list(range(0, 33)),
         "pick_rank": list(range(33, 42)),
         "pick_suit": list(range(42, 46)),
         "raise_points": 46,
         "fold_hand": 47,
         "accept_raise": 48}
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


class WorldBlindWatten:

    def __init__(self):
        self.LOG = logging.getLogger('blind_watten_logger')

        self.rank_declarer = np.random.randint(0, 4)
        self.suit_declarer = (self.rank_declarer + 3) % 4

        self.current_player = self.rank_declarer

        # init deck
        self.deck = list(range(33))
        np.random.shuffle(self.deck)

        # init starting hands
        self.hands = [[], [], [], []]

        # give cards to players
        self.hands[0] += self.deck[-5:]
        self.deck = self.deck[:-5]
        self.hands[1] += self.deck[-5:]
        self.deck = self.deck[:-5]
        self.hands[2] += self.deck[-5:]
        self.deck = self.deck[:-5]
        self.hands[3] += self.deck[-5:]
        self.deck = self.deck[:-5]

        # init board
        self.played_cards = []

        # init player scores, needs 3 for winning the hand
        self.score_team_0 = 0
        self.score_team_1 = 0

        # is True only if the last move was a raise
        self.is_last_move_raise = False
        self.is_last_move_accepted_raise = False

        # needed to understand whether a player can raise again
        self.last_accepted_raise = None

        # raise in last hand implies some specific rules. see act method
        self.is_last_hand_raise_valid = None

        # first and last card in deck (doesn't really matter where those cards are taken :D )
        self.first_card_deck = self.deck[-1:][0]
        self.deck = self.deck[:-1]
        self.last_card_deck = self.deck[-1:][0]
        self.deck = self.deck[:-1]

        self.rank = None  # schlag
        self.suit = None  # farb

        self.card_to_win = None
        self.player_winning = None

        self.current_game_prize = 2

        for card in self.hands[0]:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)
        for card in self.hands[1]:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)
        for card in self.hands[2]:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)
        for card in self.hands[3]:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)

        # player who won the game
        self.winning_team = None

        self.moves = moves

        # list of actions taken in a game, used for debugging purposes
        self.moves_series = []
        self.starting_state = f"\nSTARTING STATE\n{self.current_player}, {self.rank_declarer}, {self.suit_declarer} \n " \
                              f"{self.hands}\n" \
                              f" {self.played_cards}, {self.score_team_0}, {self.score_team_1}, {self.current_game_prize}\n " \
                              f"{self.is_last_move_raise}, {self.is_last_move_accepted_raise}," \
                              f" {self.is_last_hand_raise_valid}, {self.first_card_deck}, {self.last_card_deck}," \
                              f" {self.rank}, {self.suit}"

    def get_valid_moves_zeros(self):
        valid_moves = self.get_valid_moves()
        if len(valid_moves) == 0:
            self.display()
            raise ValidMovesError("Valid moves cannot be 0!")
        valid_moves_zeros = [0] * 50  # number of possible moves
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
            augmented_valid_moves = self._augment_valid_moves(valid_moves)
            self.LOG.debug(f"Valid moves for player [{self.current_player}] are {augmented_valid_moves}")
            return augmented_valid_moves

        # player that has not given cards declare the rank and can't raise
        if self.rank is None:
            valid_moves = self.moves["pick_rank"]
            self.LOG.debug(f"Valid moves for player [{self.current_player}] are {valid_moves}")
            return valid_moves

        # player that has given cards declare the suit. If weli was chosen as rank, then suit is irrelevant
        if self.suit is None:
            valid_moves = self.moves["pick_suit"]
            self.LOG.debug(f"Valid moves for player [{self.current_player}] are {valid_moves}")
            return valid_moves

        # list to be returned
        valid_moves = []

        current_hand = self.hands[self.current_player]

        # when the cards in game are divisible by four, then no hand has been played or one has just finished so
        # any card in hand of the current player can be played
        # the same goes when the player does not know the rank and the suit
        if (len(self.played_cards) % 4) == 0 or \
                (self.current_player != self.rank_declarer and self.current_player != self.suit_declarer):
            augmented_valid_moves = self._augment_valid_moves(current_hand)
            self.LOG.debug(f"Valid moves for player [{self.current_player}] are {augmented_valid_moves}")
            return augmented_valid_moves

        # at this point the first card that is in the table must be taken in consideration
        played_rank, played_suit = get_rs(self._get_first_played_card())

        for card in current_hand:
            card_rank, card_suit = get_rs(card)

            # if a player plays a card of the chosen suit, the opponent should play a card of the same rank or a card
            # of the chosen rank
            if played_suit == self.suit and card_suit == played_suit:
                valid_moves.append(card)
                # print("1: rank {} --- suit {}".format(card_rank, card_suit))
            # card of the chosen rank (blinden)
            elif card_rank == self.rank:
                valid_moves.append(card)
                # print("2: rank {} --- suit {}".format(card_rank, card_suit))
            elif played_suit != self.suit:
                valid_moves.append(card)
                # print("3: rank {} --- suit {}".format(card_rank, card_suit))

        # if the player has two cards and these are the rechte and the guate
        # then it can play any card of the hand
        if len(valid_moves) == 2:
            card_rank_0, card_suit_0 = get_rs(valid_moves[0])
            card_rank_1, card_suit_1 = get_rs(valid_moves[1])
            if (self.is_guate(card_rank_0, card_suit_0) and self.is_rechte(card_rank_1, card_suit_1)) or \
                    (self.is_rechte(card_rank_0, card_suit_0) and self.is_guate(card_rank_1, card_suit_1)):
                augmented_valid_moves = self._augment_valid_moves(current_hand)
                self.LOG.debug(f"Valid moves for player [{self.current_player}] are {augmented_valid_moves}")
                return augmented_valid_moves

        # if the opponent has only the rechte or the guate in his hand with the same played suit,
        # then he is not forced to play it
        if len(valid_moves) == 1:
            card_rank, card_suit = get_rs(valid_moves[0])
            if self.is_rechte(card_rank, card_suit) or self.is_guate(card_rank, card_suit):
                augmented_valid_moves = self._augment_valid_moves(current_hand)
                self.LOG.debug(f"Valid moves for player [{self.current_player}] are {augmented_valid_moves}")
                return augmented_valid_moves

        if len(valid_moves) == 0:
            valid_moves = current_hand

        augmented_valid_moves = self._augment_valid_moves(valid_moves)
        self.LOG.debug(f"Valid moves for player [{self.current_player}] are {augmented_valid_moves}")
        return augmented_valid_moves

    def _augment_valid_moves(self, mov):
        valid_moves = []
        valid_moves.extend(mov)
        # teams can raise alternately
        # !!COMMENTED TO LEARN FIRST HOW TO PLAY CARDS!!
        if (self.is_last_hand_raise_valid is None) and \
                (self.is_last_move_raise or self.last_accepted_raise == self.current_player % 2) and \
                (self.current_game_prize < 15):
            valid_moves.append(self.moves["raise_points"])
        return valid_moves

    # make a single move and apply changes to inner state of the world
    # modify the current state of the game and returns an outcome
    # the function should return 2 values: the outcome of the move and the next player
    # the outcome should be wither
    # - end, a single game is ended because one of the 2 players won 3 hands or a player folds
    # - continue, a player made a move that didn't bring the current game to an end
    # - current_player_won
    # the next player can be either 0, 1, 2 or 3
    def act(self, action):
        num_played_cards = len(self.played_cards)
        if action not in self.get_valid_moves():
            raise InvalidActionError("Action %d cannot be played" % action)
        if action > 48:
            raise InvalidActionError("Action %d is not valid" % action)
        if self.score_team_0 > 3 or self.score_team_1 > 3:
            raise InconsistentStateError("Current game score cannot exceed 3. Player 1 [%d] and player -1 [%d]"
                                         % (self.score_team_0, self.score_team_1))

        self.moves_series.append(action)

        if action == moves["raise_points"]:
            if self.is_last_hand_raise_valid is not None:
                raise InvalidActionError("Cannot raise if the previous move was a last hand raise")
            self.LOG.debug(f"{self.current_player} raised points")

            self.is_last_move_raise = True
            self.is_last_move_accepted_raise = False
            if num_played_cards >= 16:
                self.is_last_hand_raise_valid = self._last_hand_raise_valid()
            self.current_game_prize += 1
            return self._act_continue_move()

        if action == moves["accept_raise"]:
            if self.is_last_move_raise is False or self.is_last_move_accepted_raise:
                raise InvalidActionError("Cannot accept raise if the previous move was not a raise")
            self.LOG.debug(f"{self.current_player} accepted raise")
            self.is_last_move_accepted_raise = True
            self.last_accepted_raise = self.current_player % 2
            self.is_last_move_raise = False
            return self._act_continue_move()

        # if a player folds, then the prize is given to the opponent
        if action == moves["fold_hand"]:
            if self.is_last_move_raise is False or self.is_last_move_accepted_raise:
                raise InvalidActionError("Cannot fold hand if the previous move was not a raise")
            self.LOG.debug(f"{self.current_player} folds hand")
            self._assign_points_fold()
            return "end", self.current_player

        # if an action is not a raise, an accept raise or a fold, then the next move is definitely going to
        # reset the chance for raising
        self.is_last_move_accepted_raise = False
        self.is_last_move_raise = False

        if action in moves["play_card"]:
            if self.is_last_move_raise:
                raise InvalidActionError("Cannot play a card if the previous move was a raise")

            self.LOG.debug(f"{self.current_player} played card [{action}]")

            hand = self.hands[self.current_player]
            if action not in hand:
                self.display()
                raise InconsistentStateError(
                    'Played card [%d] not in %s of player %d' % (action, hand, self.current_player))

            self._remove_card_from_hand(action, self.current_player)

            # played cards are 16 and current player also raised without respecting the conditions
            if self.is_last_hand_raise_valid is not None and not self.is_last_hand_raise_valid:
                if self.current_player % 2 == 1:
                    self.winning_team = 0
                else:
                    self.winning_team = 1
                return "end", self.current_player

            if num_played_cards % 4 == 0:
                self.played_cards.append(action)
                self.card_to_win = action
                self.player_winning = self.current_player
                return self._act_continue_move()
            elif num_played_cards % 4 != 3:
                self.played_cards.append(action)
                if not self.compare_cards(self.card_to_win, action):
                    self.card_to_win = action
                    self.player_winning = self.current_player
                return self._act_continue_move()
            else:
                self.played_cards.append(action)
                if not self.compare_cards(self.card_to_win, action):
                    self.player_winning = self.current_player

                if self.player_winning % 2 == 0:
                    self.score_team_0 += 1
                else:
                    self.score_team_1 += 1

                if self.score_team_0 == 3 or self.score_team_1 == 3:
                    return self._hand_is_done_after_card_is_played_common()

                self.current_player = self.player_winning
                return "continue", self.player_winning

        if action in moves["pick_suit"]:
            if self.is_last_move_raise:
                raise InvalidActionError("Cannot raise before picking suit")

            self.suit = action % 42
            self.LOG.debug(f"{self.current_player} picked suit [{self.suit}]")
            return self._act_continue_move()

        if action in moves["pick_rank"]:
            if self.is_last_move_raise:
                raise InvalidActionError("Cannot raise before picking rank")

            self.rank = action % 33
            self.LOG.debug(f"{self.current_player} picked rank [{self.rank}]")
            return self._act_continue_move()

        self.display()
        raise InconsistentStateError("Action %d is not allowed." % action)

    def _act_continue_move(self):
        self.current_player = (self.current_player + 1) % 4
        return "continue", self.current_player

    def _hand_is_done_after_card_is_played_common(self):
        if self.score_team_0 >= 3:
            self.winning_team = 0
        elif self.score_team_1 >= 3:
            self.winning_team = 1
        return "end", self.current_player

    def _remove_card_from_hand(self, action, player):
        if player < 0 or player > 3:
            raise InvalidActionError("Player should be either 1 or -1. Got %d" % player)
        self.hands[player].remove(action)

    # if a player folds, then the hand is over with the raised prize - 1 for the opponent team
    # except when the raise was done in a not valid situation
    def _assign_points_fold(self):
        self.current_game_prize = self.current_game_prize - 1
        if self.is_last_hand_raise_valid is None or self.is_last_hand_raise_valid:
            self.winning_team = (self.current_player + 1) % 2
        else:
            self.winning_team = self.current_player % 2

    # returns true if the player who raised the current turn satisfies the following rules:
    # - he has a trumpf
    # - his card has the same suit of the one played by the previous player
    # - his card wins against the one played by the opponent player
    # or when the player does not know the rank and the suit
    def _last_hand_raise_valid(self):
        num_played_cards = len(self.played_cards)

        if 16 <= num_played_cards <= 19:
            raise InconsistentStateError(
                "Num played cards when fold occurs in last hand can be 16, 17, 18, 19. Got %d." % num_played_cards)

        if self.current_player != self.rank_declarer and self.current_player != self.suit_declarer:
            return True

        hidden_card = self.hands[self.current_player][0]
        hidd_r, hidd_s = get_rs(hidden_card)

        if self.is_trumpf(hidd_r, hidd_s):
            return True
        if num_played_cards % 4 > 0:
            _, first_card_suit = get_rs(self._get_first_played_card())
            if not self.compare_cards(self.card_to_win, hidden_card) or hidd_s == first_card_suit:
                return True

        return False

    # routine for deciding whether a card (card1) wins over another card (card2)
    # returns true if the first card wins, false otherwise
    # the first card is expected to be played before the second one
    #
    # ORDER OF IMPORTANCE:
    # - Guate (card with the same suit of the chosen suit and 1 rank higher of the rechte)
    # - Rechte (card with the same suit and rank chosen when the game started)
    # - Blinden (cards with the same rank of the chosen rank)
    # - Trümpfe (cards with the same suit of the chosen suit)
    # - Other cards (importance given by the rank)
    def compare_cards(self, card1, card2):

        card1_rank, card1_suit = get_rs(card1)
        card2_rank, card2_suit = get_rs(card2)

        #######################################################
        # GUATE
        #######################################################

        # guate is the strongest card
        if self.is_guate(card1_rank, card1_suit):
            return True
        if self.is_guate(card2_rank, card2_suit):
            return False

        #######################################################
        # RECHTE
        #######################################################

        # rechte is the second strongest card
        if self.is_rechte(card1_rank, card1_suit):
            return True
        if self.is_rechte(card2_rank, card2_suit):
            return False

        #######################################################
        # BLINDEN
        #######################################################

        # the third strongest cards after the rechte are the blinde
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

    def is_guate(self, card_rank, card_suit):
        # if the rechte is the weli, there is no guate
        if self.rank == 8:
            return False
        elif self.suit == card_suit and (self.rank + 1) % 8 == card_rank:
            return True
        else:
            return False

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
        if self.score_team_0 == 3 or self.score_team_1 == 3 or self.winning_team is not None:
            return True
        else:
            return False

    # this is called after act, player is the next player
    def is_won(self, player):
        if not 0 < player < 4:
            raise InvalidInputError("Player should be either 0, 1, 2 or 3. Input is %d." % player)

        if self.score_team_0 >= 3 and self.score_team_1 >= 3:
            raise InconsistentStateError("Both teams cannot exceed score threshold. Only one winner is allowed.")
        if player % 2 == 0 and self.score_team_0 >= 3:
            return True
        if player % 2 == 1 and self.score_team_1 >= 3:
            return True
        return False

    def get_player(self):
        return self.current_player

    # should return a unique id with the state of the game
    # the needed info are:
    # - first card of the deck (for all players) (list of 33)
    # - last card of the deck (for the player who distributed cards) (list of 33)
    # - cards in hand (list of 33)
    # - picked rank for rank and suit declarers(list of 9)
    # - picked suit for rank and suit declarers(list of 4)
    # - winning card (list of 33)
    # - played cards (list of 33)
    # - points current hand current team (max 2)
    # - points current hand opponent team (max 2)
    # - last move raise (1)
    # - last move accepted raise (1)
    # - last move valid raise (1)
    # - current prize (13)
    # total array length: 198
    def observe(self, player):
        if not 0 <= player <= 3:
            raise InvalidInputError("Player should be either 0, 1, 2 or 3. Input is %d." % player)

        observation = np.zeros((198,))

        # first card deck
        observation[self.first_card_deck] = 1

        # last card deck
        index = 33
        if player == self.suit_declarer:
            observation[index + self.last_card_deck] = 1

        # cards in hand
        index += 33  # 66
        hand = self.hands[player]
        for card in hand:
            observation[index + card] = 1

        # picked rank
        index += 33  # 99
        if self.rank is not None and (player == self.rank_declarer or player == self.suit_declarer):
            observation[index + self.rank] = 1

        # picked suit
        index += 9  # 108
        if self.suit is not None and (player == self.rank_declarer or player == self.suit_declarer):
            observation[index + self.suit] = 1

        # winning card
        index += 4  # 112
        if len(self.played_cards) % 4 > 0:
            observation[index + self.card_to_win()] = 1

        # played cards
        index += 33  # 145
        for card in self.played_cards:
            observation[index + card] = 1

        # points current hand current player
        index += 33  # 178
        points_current_hand_current = self.score_team_0 if player % 2 == 0 else self.score_team_1
        if points_current_hand_current != 0:
            observation[index + points_current_hand_current - 1] = 1

        # points current hand opponent player
        index += 2  # 180
        points_current_hand_opponent = self.score_team_1 if player % 2 == 0 else self.score_team_0
        if points_current_hand_opponent != 0:
            observation[index + points_current_hand_opponent - 1] = 1

        index += 2  # 182
        if self.is_last_move_raise:
            observation[index] = 1

        index += 1  # 183
        if self.is_last_move_accepted_raise:
            observation[index] = 1

        index += 1  # 184
        if self.is_last_hand_raise_valid is None:
            observation[index] = 0
        else:
            observation[index] = 1

        index += 1  # 185
        if self.current_game_prize - 3 >= 0:
            observation[index + self.current_game_prize - 3] = 1

        # total size = 185 + 13 = 198

        observation = observation.reshape((198, 1))
        return observation

    def _get_first_played_card(self):
        num_cards_on_the_table = len(self.played_cards) % 4
        return self.played_cards[-num_cards_on_the_table]

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
