import { Component, Input } from '@angular/core';
import { GameState, GameStateService } from '../../services/game-state.service';
import { Player, PlayerBoxScore } from '../../services/stats.service';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-scoreboard',
  standalone: true,
  imports: [NgFor],
  templateUrl: './scoreboard.component.html',
  styleUrl: './scoreboard.component.scss',
})
export class ScoreboardComponent {
  @Input() user!: number;
  gameState: GameState;
  players: Player[] = [];

  constructor(gameStateService: GameStateService) {
    this.gameState = gameStateService.gameState;
  }

  ngOnInit() {
    if (this.user === 1) {
      this.players = this.gameState.playerOneRoster.players.map((player) => {
        return player;
      });
    }
    if (this.user === 2) {
      this.players = this.gameState.playerTwoRoster.players.map((player) => {
        return player;
      });
    }
  }
}
