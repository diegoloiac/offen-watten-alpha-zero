import {GameState} from "../app/model/game-state";
import {GameStateMoveResult} from "../app/model/game-state-move-result";

export interface IAppState {
  game_id: string;
  current_state: GameState;
  next_states: GameStateMoveResult[];
  game_description: string;
  player_distributes_cards: boolean;
  valid_moves: number[];
}
