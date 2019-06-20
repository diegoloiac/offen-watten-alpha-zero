import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "../../environments/environment";
import {StartGamePayloadRes} from "./model/start-game-payload-res";
import {WattenResponse} from "./model/response";
import {StartGamePayloadReq} from "./model/start-game-payload-req";
import {NgRedux} from "@angular-redux/store";
import {IAppState} from "../../redux/IAppState";
import {ValidMovesPayloadRes} from "./model/valid-moves-payload-res";

@Injectable({providedIn: 'root'})
export class WattenGameService {

  constructor(private http: HttpClient, private ngRedux: NgRedux<IAppState>) {
  }

  public startGame(playerDistributesCards: boolean): Observable<WattenResponse<StartGamePayloadRes>> {
    let url: string = `${environment.apiPrefix}/game`;
    let payload: StartGamePayloadReq = new StartGamePayloadReq();
    payload.player_distributes_cards = playerDistributesCards;
    return this.http.put<WattenResponse<StartGamePayloadRes>>(url, payload);
  }

  public quitGame(gameId: string): Observable<any> {
    let url: string = `${environment.apiPrefix}/game/${gameId}`;
    return this.http.delete<Observable<any>>(url);
  }

  public getAvailableMoves(): Observable<WattenResponse<ValidMovesPayloadRes>> {
    let url: string = `${environment.apiPrefix}/moves/${this.ngRedux.getState().game_id}`;
    return this.http.get<WattenResponse<ValidMovesPayloadRes>>(url);
  }

}
