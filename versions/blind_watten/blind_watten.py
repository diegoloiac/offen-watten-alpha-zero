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

        self.current_player = 0
        self.rank_declarer = 0
        self.suit_declarer = (self.rank_declarer + 1) % 4

        # init deck
        self.deck = list(range(33))
        np.random.shuffle(self.deck)

        # init starting hands
        self.hand_player_0 = []
        self.hand_player_1 = []
        self.hand_player_2 = []
        self.hand_player_3 = []

        # give cards to players
        self.hand_player_0 += self.deck[-5:]
        self.deck = self.deck[:-5]
        self.hand_player_1 += self.deck[-5:]
        self.deck = self.deck[:-5]
        self.hand_player_2 += self.deck[-5:]
        self.deck = self.deck[:-5]
        self.hand_player_3 += self.deck[-5:]
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

        self.current_game_prize = 2

        for card in self.hand_player_0:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)
        for card in self.hand_player_1:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)
        for card in self.hand_player_2:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)
        for card in self.hand_player_3:
            if card in self.deck:
                raise InconsistentStateError("Card %d cannot be in deck." % card)

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

        current_hand = self._get_current_player_hand()

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
            if self.suit == card_suit_0 and self.suit == card_suit_1 and \
                    ((self.rank == card_rank_0 and self._is_guate_rank(card_rank_1)) or
                     (self.rank == card_rank_1 and self._is_guate_rank(card_rank_0))):
                augmented_valid_moves = self._augment_valid_moves(current_hand)
                self.LOG.debug(f"Valid moves for player [{self.current_player}] are {augmented_valid_moves}")
                return augmented_valid_moves

        # if the opponent has only the rechte or the guate in his hand with the same played suit,
        # then he is not forced to play it
        if len(valid_moves) == 1:
            card_rank, card_suit = get_rs(valid_moves[0])
            if self.suit == card_suit and (self.rank == card_rank or self._is_guate_rank(card_rank)):
                augmented_valid_moves = self._augment_valid_moves(current_hand)
                self.LOG.debug(f"Valid moves for player [{self.current_player}] are {augmented_valid_moves}")
                return augmented_valid_moves

        if len(valid_moves) == 0:
            valid_moves = current_hand

        augmented_valid_moves = self._augment_valid_moves(valid_moves)
        self.LOG.debug(f"Valid moves for player [{self.current_player}] are {augmented_valid_moves}")
        return augmented_valid_moves



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
