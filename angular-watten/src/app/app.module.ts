import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {NewGameComponent} from './new-game/new-game.component';

import {NgReduxModule, NgRedux} from '@angular-redux/store';
import {rootReducer} from "../redux/rootReducer";
import {IAppState} from "../redux/IAppState";
import {HttpClientModule} from "@angular/common/http";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatButtonModule} from "@angular/material";

@NgModule({
  declarations: [
    AppComponent,
    NewGameComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,

    NgReduxModule,
    HttpClientModule,

    BrowserAnimationsModule,
    MatButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(ngRedux: NgRedux<IAppState>) {
    ngRedux.configureStore(rootReducer, {}, []);
  }
}
