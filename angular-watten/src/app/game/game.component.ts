import {Component, OnInit} from '@angular/core';
import Deck from 'deck-of-cards';
import Card from 'deck-of-cards';
import {NgRedux, select} from "@angular-redux/store";
import {Observable} from "rxjs";
import {GameState} from "../model/game-state";
import {IAppState} from "../../redux/IAppState";
import {isNullOrUndefined} from "util";
import {UpdateGameDescAction} from "../../redux/actions/update-game-desc-action";
import {GameStateMoveResult} from "../model/game-state-move-result";
import {UpdateGameStateAction} from "../../redux/actions/update-game-state-action";
import {WattenGameService} from "../service/watten-game.service";
import {ValidMovesAction} from "../../redux/actions/valid-moves-action";
import {BlockUI, NgBlockUI} from "ng-block-ui";
import {Router} from "@angular/router";

declare var $: any; // jquery

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {

  @BlockUI() blockUI: NgBlockUI;

  moveQueue: GameStateMoveResult[] = [];

  ranksAndSuits = [
    {'label': '7', 'value': 33},
    {'label': '8', 'value': 34},
    {'label': '9', 'value': 35},
    {'label': '10', 'value': 36},
    {'label': 'unter', 'value': 37},
    {'label': 'ober', 'value': 38},
    {'label': 'kining', 'value': 39},
    {'label': 'ass', 'value': 40},
    {'label': 'weli', 'value': 41},

    {'label': 'spades', 'value': 42},
    {'label': 'hearts', 'value': 43},
    {'label': 'clubs', 'value': 44},
    {'label': 'diamonds', 'value': 45}
  ];

  raiseMoves = [
    {'label': 'Raise points', 'value': 46},
    {'label': 'Fold hand', 'value': 47},
    {'label': 'Accept raise', 'value': 48}
  ];

  displayLastCardDesc: boolean;
  lockPlayerMoves: boolean = true;

  $cardContainer: any;
  deck: Deck;

  playedCards: any[] = [];

  isGameAlreadyStarted: boolean = false;

  @select(['valid_moves']) readonly $validMoves: Observable<number[]>;

  @select(['game_description']) readonly $gameDescription: Observable<string>;

  @select(['current_state', 'player_A_score']) readonly $playerScore: Observable<number>;
  @select(['current_state', 'player_B_score']) readonly $opponentScore: Observable<number>;
  @select(['current_state', 'current_game_prize']) readonly $currentGamePrize: Observable<number>;
  @select(['current_state', 'suit']) readonly $suit: Observable<number>;
  @select(['current_state', 'rank']) readonly $rank: Observable<number>;

  constructor(private ngRedux: NgRedux<IAppState>,
              private updateGameDescAction: UpdateGameDescAction,
              private updateGameStateAction: UpdateGameStateAction,
              private validMovesAction: ValidMovesAction,
              private wattenGameService: WattenGameService,
              private router: Router) {
  }

  ngOnInit() {
    this.refreshTable();
  }

  private refreshTable(): void {
    if (!isNullOrUndefined(this.deck)) {
      this.deck.unmount();
    }

    // refresh variables
    this.lockPlayerMoves = true;
    this.$cardContainer = undefined;
    this.deck = undefined;
    this.playedCards = [];
    this.isGameAlreadyStarted = false;


    // init state of the game
    let startingPlayerHand: number[] = this.ngRedux.getState().current_state.player_hand;
    let startingOpponentHand: number[] = this.ngRedux.getState().current_state.opponent_hand;
    let firstCardDeck: number = this.ngRedux.getState().current_state.first_card_deck;
    let lastCardDeck: number = this.ngRedux.getState().current_state.last_card_deck;
    if (isNullOrUndefined(lastCardDeck)) {
      this.displayLastCardDesc = false;
    } else {
      this.displayLastCardDesc = true;
    }

    let playerFirstMove: boolean = this.ngRedux.getState().player_distributes_cards;
    if (!playerFirstMove) {
      this.updateAvailableMoves();
    }

    this.$cardContainer = document.getElementById('card-container');
    this.deck = Deck();

    this.keepOnlyWattenCardsInDeck(this.deck);

    this.deck.mount(this.$cardContainer);

    this.deck.sort();

    this.changeCardsPositionInDeck(this.deck, startingPlayerHand, startingOpponentHand, firstCardDeck, lastCardDeck);

    setTimeout(() => this.distributeCards(lastCardDeck), 1000);

    this.blockUI.stop();
  }

  // returne a boolean that states whether the game interaction should continue
  public makeMove(move?: number): void {
    if (this.playedCards.length == 2) {
      this.playedCards.forEach((card) => {
        card.animateTo({
          delay: 100,
          duration: 300,
          ease: 'quintOut',

          x: -400,
          y: 0
        });
        card.setSide('back');
      });
      this.playedCards.length = 0;
    }

    if (this.moveQueue.length > 0) {
      let stateMoveResult: GameStateMoveResult = this.moveQueue.pop();
      this.makeMoveAux(stateMoveResult);
      if (this.moveQueue.length == 0) {
        this.updateAvailableMoves();
      }
      return;
    }

    this.wattenGameService.makeMove(move).subscribe(res => {
      this.ngRedux.dispatch(this.validMovesAction.updateValidMoves([]));
      res.body = res.body.reverse();
      let stateMoveResult: GameStateMoveResult = res.body.pop();
      this.makeMoveAux(stateMoveResult);
      res.body.forEach((state) => {
        this.moveQueue.push(state);
      });
      if (this.moveQueue.length > 0) {
        this.lockPlayerMoves = true;
      } else if (move < 33) {
        this.updateAvailableMoves();
      }
    });
  }

  private checkGameEnded(result: string): boolean {
    if (result === 'player_won') {
      alert("You won!");
      this.wattenGameService.quitGame(this.ngRedux.getState().game_id).subscribe(() => {
        this.router.navigateByUrl('/');
      });
      return true;
    } else if (result === 'opponent_won') {
      alert("Opponent won!");
      this.wattenGameService.quitGame(this.ngRedux.getState().game_id).subscribe(() => {
        this.router.navigateByUrl('/');
      });
      return true;
    }
    return false;
  }

  private makeMoveAux(stateMoveResult: GameStateMoveResult): void {
    this.ngRedux.dispatch(this.updateGameStateAction.updateGameState(stateMoveResult.state));
    if (this.checkGameEnded(stateMoveResult.game_result)) {
      return;
    }
    // move card
    if (stateMoveResult.move < 33) {
      let coords = this.playedCardCoordinates(stateMoveResult.state);
      if (stateMoveResult.player == 1) { // opponent
        this.deck.cards.forEach((card) => {
          if (card.i == stateMoveResult.move) {
            card.animateTo({
              delay: 100,
              duration: 300,
              ease: 'quintOut',

              x: coords.x,
              y: coords.y
            });
            card.setSide('front');
            this.playedCards.push(card);
          }
        });
      }
    }

    // dispatch new game description
    let whoPlayedMoveDesc = stateMoveResult.player == 0 ? 'You' : 'Opponent';
    let actionMoveDesc: string;
    if (stateMoveResult.move < 33) {
      actionMoveDesc = 'played card';
    } else if (stateMoveResult.move < 42) {
      actionMoveDesc = 'picked rank';
    } else if (stateMoveResult.move < 46) {
      actionMoveDesc = 'picked suit';
      this.isGameAlreadyStarted = true; // used for refreshing state after hand
    } else if (stateMoveResult.move == 46) {
      actionMoveDesc = 'raised points';
    } else if (stateMoveResult.move == 47) {
      actionMoveDesc = 'folded hand';
      this.refreshTable();
    } else if (stateMoveResult.move == 48) {
      actionMoveDesc = 'accepted raise';
    } else if (stateMoveResult.move == 49) {
      actionMoveDesc = 'folded and forced to show hand';
    }
    // updates the state of the game
    this.ngRedux.dispatch(this.updateGameDescAction.updateGameDesc(`${whoPlayedMoveDesc} ${actionMoveDesc}`))
  }

  private playedCardCoordinates(state: GameState): any {
    if ((this.playedCards.length % 2) == 0) {
      return {x: 100, y: 0}
    } else {
      return {x: 180, y: 0}
    }
  }

  public shouldShowActionButton(move: number): boolean {
    for (let rankOrSuit of this.ranksAndSuits) {
      if (rankOrSuit.value == move) {
        return true;
      }
    }
    for (let raiseMove of this.raiseMoves) {
      if (raiseMove.value == move) {
        return true;
      }
    }
    return false;
  }

  public getLabelMove(move: number): string {
    for (let rankOrSuit of this.ranksAndSuits) {
      if (rankOrSuit.value == move) {
        return rankOrSuit.label;
      }
    }
    for (let raiseMove of this.raiseMoves) {
      if (raiseMove.value == move) {
        return raiseMove.label;
      }
    }
    return "NONE";
  }

  private lastCardClicked(): void {
    let nextStates: GameStateMoveResult[] = this.ngRedux.getState().next_states;
    this.displayLastCardDesc = false;
    if (isNullOrUndefined(nextStates)) {
      return;
    }
    if (nextStates.length > 1) {
      console.error("next states cannot be more than 1 when last card is clicked");
    }
    let nextStateMoveResult: GameStateMoveResult = nextStates[0];
    let playedMoveByOpponent: number = nextStateMoveResult.move;
    if (playedMoveByOpponent == 46) { // raise points
      this.ngRedux.dispatch(this.updateGameDescAction.updateGameDesc("Opponent raised"));
    } else {
      this.ngRedux.dispatch(this.updateGameDescAction.updateGameDesc("Opponent picked rank"));
    }
    this.ngRedux.dispatch(this.updateGameStateAction.updateGameState(nextStateMoveResult.state));

    this.updateAvailableMoves();
  }

  private distributeCards(lastCardDeckId: number): void {
    // distributes cards to player
    let x_player = -160;
    let y_player = 200;
    for (let i = 0; i < 5; i++) {
      let cardTemp: any = this.deck.cards[i];

      cardTemp.animateTo({
        delay: 1000 + i * 2, // wait 1 second + i * 2 ms
        duration: 500,
        ease: 'quintOut',

        x: x_player,
        y: y_player
      });
      cardTemp.setSide('front');
      x_player += 80;

      $(cardTemp.$el).click(() => {
        if (!this.lockPlayerMoves) {
          let validMoves: number[] = this.ngRedux.getState().valid_moves;
          if (validMoves.includes(cardTemp.i)) {
            this.makeMove(cardTemp.i);
            let currentState: GameState = this.ngRedux.getState().current_state;
            let coord: any = this.playedCardCoordinates(currentState);
            cardTemp.animateTo({
              delay: 100,
              duration: 300,
              ease: 'quintOut',

              x: coord.x,
              y: coord.y
            });
            this.playedCards.push(cardTemp);
          } else {
            alert("Invalid move");
          }
        }
      });
    }

    // distributes cards to opponent
    let x_opp = -160;
    let y_opp = -200;
    for (let i = 7; i < 12; i++) {
      this.deck.cards[i].animateTo({
        delay: 1000 + i * 2, // wait 1 second + i * 2 ms
        duration: 500,
        ease: 'quintOut',

        x: x_opp,
        y: y_opp
      });
      x_opp += 80
    }

    // show first card of deck
    this.deck.cards[5].animateTo({
      delay: 1000,
      duration: 500,
      ease: 'quintOut',

      x: -100,
      y: 0
    });
    this.deck.cards[5].setSide('front');

    // show last card, if present
    if (!isNullOrUndefined(lastCardDeckId)) {
      this.deck.cards[6].animateTo({
        delay: 1000,
        duration: 500,
        ease: 'quintOut',

        x: -400,
        y: 0
      });
      this.deck.cards[6].setSide('front');
      $(this.deck.cards[6].$el).click(() => {
        this.deck.cards[6].unmount();
        this.lastCardClicked();
      });

    }

  }

  private keepOnlyWattenCardsInDeck(deck: Deck): void {
    let cardsToKeep: any[] = [];
    deck.cards.forEach((card, i) => {
      if (card.rank == 2 || card.rank == 3 || card.rank == 4 || card.rank == 5) {
        card.unmount();
        return;
      }
      if (card.rank == 6 && card.suit != 3) {
        card.unmount();
        return;
      }
      cardsToKeep.push(card);
    });
    this.changeElementPosition(cardsToKeep, 0, 7); // move ace of ♠︎
    this.changeElementPosition(cardsToKeep, 8, 15); // move ace of ♥︎
    this.changeElementPosition(cardsToKeep, 16, 23); // move ace of ♣︎︎
    this.changeElementPosition(cardsToKeep, 24, 32); // move ace of ♦︎
    this.changeElementPosition(cardsToKeep, 24, 32); // move weli (6 of ♦)︎
    cardsToKeep.forEach((card, i) => {
      card.i = i;
      card.pos = i;
    });
    deck.cards = cardsToKeep;
  }

  private changeCardsPositionInDeck(deck: Deck,
                                    startingPlayerHand: number[],
                                    startingOpponentHand: number[],
                                    firstCardDeckId: number,
                                    lastCardDeckId: number): void {
    // change player cards position in deck for distributing them later
    startingPlayerHand.forEach((cardId, i) => {
      deck.cards.forEach((card, y) => {
        if (card.i == cardId) {
          this.changeElementPosition(deck.cards, y, i);
        }
      });
    });

    // change first card deck position in deck
    deck.cards.forEach((card, i) => {
      if (card.i == firstCardDeckId) {
        this.changeElementPosition(deck.cards, i, 5);
      }
    });

    // change last card deck position in deck
    if (!isNullOrUndefined(lastCardDeckId)) {
      deck.cards.forEach((card, i) => {
        if (card.i == lastCardDeckId) {
          this.changeElementPosition(deck.cards, i, 6);
        }
      });
    }

    // change opponent cards position in deck for distributing them later
    startingOpponentHand.forEach((cardId, i) => {
      deck.cards.forEach((card, y) => {
        if (card.i == cardId) {
          this.changeElementPosition(deck.cards, y, i + 7);
        }
      });
    });

  }

  private changeElementPosition(arr, fromIndex, toIndex) {
    var element = arr[fromIndex];
    arr.splice(fromIndex, 1);
    arr.splice(toIndex, 0, element);
  }

  private updateAvailableMoves(): void {
    this.wattenGameService.getAvailableMoves().subscribe(res => {
      this.ngRedux.dispatch(this.validMovesAction.updateValidMoves(res.body.valid_moves));
      this.lockPlayerMoves = false;
      if (this.isGameAlreadyStarted) {
        if (res.body.valid_moves.includes(33) || res.body.valid_moves.includes(42)) {
          this.blockUI.start("Hand done. Setting up table for next hand.");
          this.refreshTable();
        }
      }
    });
  }

}
