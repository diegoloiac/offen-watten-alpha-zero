import {IAppState} from "./IAppState";
import {AnyAction} from "redux";
import {StartGameActions} from "./actions/start-game-actions";
import {UpdateGameDescAction} from "./actions/update-game-desc-action";
import {UpdateGameStateAction} from "./actions/update-game-state-action";

export function rootReducer(lastState: IAppState, action: AnyAction): IAppState {
  switch (action.type) {
    case StartGameActions.START_GAME:
      console.log(`START GAME action with game id [${action.extraProps.gameId}]`);
      return {
        game_id: action.extraProps.gameId,
        current_state: action.extraProps.startingState,
        next_states: action.extraProps.nextStates,
        game_description: lastState.game_description,
        player_distributes_cards: lastState.player_distributes_cards,
        valid_moves: lastState.valid_moves
      };
    case StartGameActions.QUIT_GAME:
      return {
        game_id: undefined,
        current_state: undefined,
        next_states: undefined,
        game_description: lastState.game_description,
        player_distributes_cards: lastState.player_distributes_cards,
        valid_moves: lastState.valid_moves
      };
    case UpdateGameDescAction.UPDATE_GAME_DESC:
      return {
        game_id: lastState.game_id,
        current_state: lastState.current_state,
        next_states: lastState.next_states,
        game_description: action.extraProps,
        player_distributes_cards: lastState.player_distributes_cards,
        valid_moves: lastState.valid_moves
      };
    case UpdateGameStateAction.UPDATE_GAME_STATE:
      return {
        game_id: lastState.game_id,
        current_state: action.extraProps,
        next_states: lastState.next_states,
        game_description: lastState.game_description,
        player_distributes_cards: lastState.player_distributes_cards,
        valid_moves: lastState.valid_moves
      }
  }

  return lastState;
}
