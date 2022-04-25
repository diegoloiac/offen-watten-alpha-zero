import numpy as np
from versions.hand_watten.hand_watten import WorldHandWatten, InvalidInputError, get_rs


class CNNHandWatten(WorldHandWatten):
    def __init__(self):
        super(CNNHandWatten, self).__init__()

    # 19 layers
    # 1 for each card in the hand       5
    # 1 whole-hand layer                6
    # 1 for first card of the deck      7
    # 1 for last card of the deck       8
    # 1 for the suit                    9
    # 1 for the rank                    10
    # 1 for all the played cards        11
    # 1 for the last played card        12
    # 1 for possible opponent's cards   13
    # 1 for the points in the hand      14
    # 1 for the opponent's points       15
    # 1 for is last move raise          16
    # 1 for is last move accepted raise 17
    # 1 for is last move raise none     18
    # 1 for current price               19
    def observe(self, player):
        if player not in [1, -1]:
            raise InvalidInputError("Player should be either 1 or -1. Input is %d." % player)

        player_hand = self.player_A_hand if player == 1 else self.player_B_hand

        observation = np.zeros((17, 17, 19))

        for idx, card in enumerate(player_hand):
            r, s = get_rs(card)
            observation[s, r, idx] = 1

        index = 5
        for card in player_hand:
            r, s = get_rs(card)
            observation[s, r, index] = 1

        index += 1  # 6

        r, s = get_rs(self.first_card_deck)
        observation[s, r, index] = 1

        index += 1  # 7

        if player == self.distributing_cards_player:
            r, s = get_rs(self.last_card_deck)
            observation[s, r, index] = 1

        index += 1  # 8
        observation[self.suit, 0:9, index] = 1

        index += 1  # 9
        observation[0:4, self.rank, index] = 1

        index += 1  # 10
        for card in self.played_cards:
            r, s = get_rs(card)
            observation[s, r, index] = 1

        index += 1  # 11
        if self._get_last_played_card() is not None:
            r, s = get_rs(self._get_last_played_card())
            observation[s, r, index] = 1

        index += 1  # 12
        possible_opponent_cards = self.player_B_hand.copy() if player == 1 else self.player_A_hand.copy()
        if player != self.distributing_cards_player:
            possible_opponent_cards.append(self.last_card_deck)
        possible_opponent_cards.extend(self.deck)
        for card in possible_opponent_cards:
            r, s = get_rs(card)
            observation[s, r, index] = 1

        index += 1  # 13
        points_current_hand_current = self.current_game_player_A_score if player == 1 \
            else self.current_game_player_B_score
        if points_current_hand_current != 0:
            for i in range(points_current_hand_current):
                observation[i, 8, index] = 1

        index += 1  # 14
        points_current_hand_opponent = self.current_game_player_B_score if player == 1 \
            else self.current_game_player_A_score
        if points_current_hand_opponent != 0:
            for i in range(points_current_hand_opponent):
                observation[i, 8, index] = 1

        index += 1  # 15
        if self.is_last_move_raise:
            observation[0:4, 0:9, index] = 1

        index += 1   # 16
        if self.is_last_move_accepted_raise:
            observation[0:4, 0:9, index] = 1

        index += 1  # 17
        if self.is_last_hand_raise_valid is not None:
            observation[0:4, 0:9, index] = 1

        index += 1  # 18
        columns = int(self.current_game_prize / 4)
        last_row = int(self.current_game_prize % 4)
        observation[0:4, 0:columns, index] = 1
        observation[0:last_row, columns, index] = 1

        # Depth: 18+1 = 19
        # Shape: (19, 17, 17) with zero padding

        return observation

    def deepcopy(self):
        new_world = CNNHandWatten()
        new_world.LOG = self.LOG
        new_world.current_player = self.current_player
        new_world.distributing_cards_player = self.distributing_cards_player
        new_world.deck = self.deck.copy()
        new_world.player_A_hand = self.player_A_hand.copy()
        new_world.player_B_hand = self.player_B_hand.copy()
        new_world.played_cards = self.played_cards.copy()
        new_world.current_game_player_A_score = self.current_game_player_A_score
        new_world.current_game_player_B_score = self.current_game_player_B_score
        new_world.current_game_prize = self.current_game_prize
        new_world.is_last_move_raise = self.is_last_move_raise
        new_world.is_last_move_accepted_raise = self.is_last_move_accepted_raise
        new_world.started_raising = self.started_raising
        new_world.first_card_deck = self.first_card_deck
        new_world.last_card_deck = self.last_card_deck
        new_world.rank = self.rank
        new_world.suit = self.suit
        new_world.is_last_hand_raise_valid = self.is_last_hand_raise_valid
        new_world.winning_player = self.winning_player

        new_world.starting_state = self.starting_state
        new_world.moves_series = self.moves_series.copy()
        return new_world
