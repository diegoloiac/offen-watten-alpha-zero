import {IAppState} from "./IAppState";
import {Action} from "redux";

export function rootReducer(lastState: IAppState, action: Action): IAppState {
  // switch (action.type) {
  //   case CounterActions.INCREMENT:
  //     return {count: lastState.count + 1};
  //   case CounterActions.DECREMENT:
  //     return {count: lastState.count - 1};
  // }

  // We don't care about any other actions right now.
  return lastState;
}
