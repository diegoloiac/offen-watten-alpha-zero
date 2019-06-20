import {Injectable} from "@angular/core";
import {AnyAction} from "redux";
import {GameState} from "../../app/model/game-state";

/**
 * Created by fmicheloni on 24/01/19.
 */
@Injectable()
export class UpdateGameStateAction {

  public static UPDATE_GAME_STATE = 'UPDATE_GAME_STATE';

  updateGameState(gameState: GameState): AnyAction {
    return {type: UpdateGameStateAction.UPDATE_GAME_STATE, extraProps: gameState};
  }

}
