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

declare var $: any; // jquery

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {

  displayLastCardDesc: boolean;

  $cardContainer: any;
  deck: Deck;

  @select(['game_description']) readonly $gameDescription: Observable<string>;

  @select(['current_state', 'player_A_score']) readonly $playerScore: Observable<number>;
  @select(['current_state', 'player_B_score']) readonly $opponentScore: Observable<number>;
  @select(['current_state', 'current_game_prize']) readonly $currentGamePrize: Observable<number>;
  @select(['current_state', 'suit']) readonly $suit: Observable<number>;
  @select(['current_state', 'rank']) readonly $rank: Observable<number>;

  constructor(private ngRedux: NgRedux<IAppState>,
              private updateGameDescAction: UpdateGameDescAction,
              private updateGameStateAction: UpdateGameStateAction) {
  }

  ngOnInit() {
    // init state of the game
    let startingPlayerHand: number[] = this.ngRedux.getState().current_state.player_hand;
    let firstCardDeck: number = this.ngRedux.getState().current_state.first_card_deck;
    let lastCardDeck: number = this.ngRedux.getState().current_state.last_card_deck;
    this.displayLastCardDesc = this.ngRedux.getState().player_distributes_cards;

    this.$cardContainer = document.getElementById('card-container');
    this.deck = Deck();

    this.keepOnlyWattenCardsInDeck(this.deck);

    this.deck.mount(this.$cardContainer);

    this.deck.sort();

    this.changeCardsPositionInDeck(this.deck, startingPlayerHand, firstCardDeck, lastCardDeck);

    setTimeout(() => this.distributeCards(lastCardDeck), 1000);
  }

  private lastCardClicked(): void {
    let nextStates: GameStateMoveResult[] = this.ngRedux.getState().next_states;
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
    this.displayLastCardDesc = false;
    this.ngRedux.dispatch(this.updateGameStateAction.updateGameState(nextStateMoveResult.state));
  }

  private distributeCards(lastCardDeckId: number): void {

    this.deck.cards.forEach((card, i) => {
      $(card.$el).click(() => {
        console.log(card.i);
      });
    });

    // distributes cards to player
    let x_player = -160;
    let y_player = 200;
    for (let i = 0; i < 5; i++) {
      this.deck.cards[i].animateTo({
        delay: 1000 + i * 2, // wait 1 second + i * 2 ms
        duration: 500,
        ease: 'quintOut',

        x: x_player,
        y: y_player
      });
      this.deck.cards[i].setSide('front');
      x_player += 80;
    }

    // distributes cards to opponent
    let x_opp = -160;
    let y_opp = -200;
    for (let i = 27; i < 32; i++) {
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

  }

  private changeElementPosition(arr, fromIndex, toIndex) {
    var element = arr[fromIndex];
    arr.splice(fromIndex, 1);
    arr.splice(toIndex, 0, element);
  }

}
