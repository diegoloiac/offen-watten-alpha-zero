export class GameState {
  player_hand: number[];
  opponent_hand: number[];
  first_card_deck: number;
  last_card_deck: number;
  current_game_player_A_score: number;
  current_game_player_B_score: number;
  player_A_score: number;
  player_B_score: number;
  played_cards: number[];
  current_game_prize: number;
  suit: number;
  rank: number;
}
