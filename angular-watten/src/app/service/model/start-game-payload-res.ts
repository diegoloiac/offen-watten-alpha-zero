import {GameState} from "../../model/game-state";
import {GameStateMoveResult} from "../../model/game-state-move-result";

export class StartGamePayloadRes {
  game_id: string;
  starting_state: GameState;
  states: GameStateMoveResult[];
}
