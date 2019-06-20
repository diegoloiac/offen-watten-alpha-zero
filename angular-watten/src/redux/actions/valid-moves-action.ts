import {Injectable} from "@angular/core";
import {AnyAction} from "redux";

/**
 * Created by fmicheloni on 24/01/19.
 */
@Injectable()
export class ValidMovesAction {

  public static VALID_MOVES = 'VALID_MOVES';

  updateValidMoves(validMoves: number[]): AnyAction {
    return {type: ValidMovesAction.VALID_MOVES, extraProps: validMoves};
  }

}
