import {Injectable} from "@angular/core";
import {AnyAction} from "redux";
import {GameState} from "../../app/model/game-state";
import {GameStateMoveResult} from "../../app/model/game-state-move-result";

/**
 * Created by fmicheloni on 24/01/19.
 */
@Injectable()
export class StartGameActions {

  public static START_GAME = 'START_GAME';
  public static QUIT_GAME = 'QUIT_GAME';

  startGame(gameId: string, startingState: GameState, nextStates: GameStateMoveResult[]): AnyAction {
    return {type: StartGameActions.START_GAME, extraProps: {'gameId': gameId, 'startingState': startingState, 'nextStates': nextStates}};
  }

  quitGame(): AnyAction {
    return {type: StartGameActions.QUIT_GAME};
  }

}
