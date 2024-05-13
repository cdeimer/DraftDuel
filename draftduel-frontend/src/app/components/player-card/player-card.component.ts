import { Component, Input } from '@angular/core';
import { Player } from '../../services/stats.service';
import { GameState, GameStateService } from '../../services/game-state.service';

@Component({
  selector: 'draft-pool-player-card',
  standalone: true,
  imports: [],
  templateUrl: './player-card.component.html',
  styleUrl: './player-card.component.scss',
})
export class PlayerCardComponent {
  @Input() player!: Player;
  @Input() gameState!: GameState;

  constructor(private gameStateService: GameStateService) {}

  onTakePlayer(player: Player) {
    console.log('Player taken:', player);
    // remove taken player from draft pool
    this.gameState.draftPool = this.gameStateService.removePlayerFromDraftPool(
      this.gameState.draftPool,
      player.id
    );
    // add taken player to player roster
    if (this.playerOneTurn()) {
      this.gameState.playerOneRoster.addPlayer(player);
    } else {
      //console.log('not implemented');
      this.gameState.playerTwoRoster.addPlayer(player);
    }
    this.gameState.currentPlayer = this.gameState.currentPlayer === 1 ? 2 : 1;
  }

  // check if player roster is at the limit for player's position
  playerNeedsPosition(position: string): boolean {
    if (this.playerOneTurn()) {
      return this.gameState.playerOneRoster
        .getPositionsNeeded()
        .includes(position);
    } else {
      return this.gameState.playerTwoRoster
        .getPositionsNeeded()
        .includes(position);
    }
  }

  playerOneTurn(): boolean {
    return this.gameState.currentPlayer === 1;
  }
}
