import {Injectable} from "@angular/core";
import {AnyAction} from "redux";

/**
 * Created by fmicheloni on 24/01/19.
 */
@Injectable()
export class UpdateGameDescAction {

  public static UPDATE_GAME_DESC = 'UPDATE_GAME_DESC';

  updateGameDesc(gameDesc: string): AnyAction {
    return {type: UpdateGameDescAction.UPDATE_GAME_DESC, extraProps: gameDesc};
  }

}
