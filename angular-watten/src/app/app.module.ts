import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';

import {NgReduxModule, NgRedux} from '@angular-redux/store';
import {rootReducer} from "../redux/rootReducer";
import {IAppState} from "../redux/IAppState";
import {HttpClientModule} from "@angular/common/http";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatButtonModule, MatSlideToggleModule, MatToolbarModule} from "@angular/material";
import {FormsModule} from "@angular/forms";
import {StartGameActions} from "../redux/actions/start-game-actions";
import {InstructionsComponent} from './instructions/instructions.component';
import {GameComponent} from './game/game.component';
import {UpdateGameDescAction} from "../redux/actions/update-game-desc-action";
import {UpdateGameStateAction} from "../redux/actions/update-game-state-action";
import {ValidMovesAction} from "../redux/actions/valid-moves-action";
import {BlockUIModule} from "ng-block-ui";

@NgModule({
  declarations: [
    AppComponent,
    InstructionsComponent,
    GameComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,

    NgReduxModule,
    HttpClientModule,
    FormsModule,

    BrowserAnimationsModule,
    MatButtonModule,
    MatToolbarModule,
    MatSlideToggleModule,

    BlockUIModule.forRoot()
  ],
  providers: [StartGameActions, UpdateGameDescAction, UpdateGameStateAction, ValidMovesAction],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(ngRedux: NgRedux<IAppState>) {
    ngRedux.configureStore(
      rootReducer,
      {
        game_id: undefined,
        current_state: undefined,
        next_states: undefined,
        game_description: undefined,
        player_distributes_cards: undefined,
        valid_moves: undefined
      },
      []
    );
  }
}
