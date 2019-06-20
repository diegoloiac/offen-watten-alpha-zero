import {Component, OnInit} from '@angular/core';
import {WattenGameService} from "./service/watten-game.service";
import {NgRedux, select} from "@angular-redux/store";
import {IAppState} from "../redux/IAppState";
import {StartGameActions} from "../redux/actions/start-game-actions";
import {Observable} from "rxjs";
import {Router} from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  playerDistributesCards: boolean = false;
  @select(['game_id']) readonly $game_id: Observable<string>;

  constructor(private wattenGameService: WattenGameService,
              private ngRedux: NgRedux<IAppState>,
              private startGameActions: StartGameActions,
              private router: Router) {
  }

  public startGame(playerDistributesCards: boolean): void {
    this.wattenGameService.startGame(playerDistributesCards).subscribe(res => {
      this.ngRedux.dispatch(this.startGameActions.startGame(res.body.game_id, res.body.starting_state, res.body.states));
      this.ngRedux.getState().player_distributes_cards = playerDistributesCards;
      this.router.navigateByUrl('/game');
    });
  }

  public quitGame(): void {
    this.wattenGameService.quitGame(this.ngRedux.getState().game_id).subscribe(res => {
      this.ngRedux.dispatch(this.startGameActions.quitGame());
      this.router.navigateByUrl('/');
    });
  }

}
