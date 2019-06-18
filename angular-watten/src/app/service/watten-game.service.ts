import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "../../environments/environment";
import {StartGamePayload} from "./start-game-payload";
import {WattenResponse} from "./response";

@Injectable({providedIn: 'root'})
export class WattenGameService {

  constructor(private http: HttpClient) {
  }

  public startGame(): Observable<WattenResponse<StartGamePayload>> {
    let url: string = `${environment.apiPrefix}/game`;
    return this.http.put<WattenResponse<StartGamePayload>>(url, null);
  }

}
