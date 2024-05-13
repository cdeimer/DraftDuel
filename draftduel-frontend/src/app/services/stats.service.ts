import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { mockPlayerPool } from '../mock_data/mock-player-pool';
import { Roster } from '../classes/roster';
import { Observable, tap } from 'rxjs';

export interface Player {
  id: string;
  name: string;
  position: string;
  season: number;
  team: string;
  fantasy_points: number;
  games_played: number;
  score?: number;
  player_box_score?: PlayerBoxScore;
}

export interface PlayerBoxScore {
  week: number;
  team: string;
  opponent: string;
  fantasy_points: number;
  pass_yards: number;
  pass_tds: number;
  pass_ints: number;
  pass_fumbles: number;
  rush_yards: number;
  rush_tds: number;
  rush_fumbles: number;
  rec_recs: number;
  rec_yards: number;
  rec_tds: number;
  rec_fumbles: number;
}

export interface PlayerPool {
  [key: string]: Player[];
  qbs: Player[];
  rbs: Player[];
  wrs: Player[];
  tes: Player[];
}

const totalPlayerPool: PlayerPool = mockPlayerPool;

@Injectable({
  providedIn: 'root',
})
export class StatsService {
  numQBs: number = 5;
  numRBs: number = 10;
  numWRs: number = 10;
  numTEs: number = 5;

  playerList: Player[] = [];

  constructor(private http: HttpClient) {}

  // get player pool from the backend /player_pool endpoint
  // make an api call to the backend to get the player pool
  getPlayerPool(): Observable<Player[]> {
    console.log('Getting player pool from backend...');
    return this.http.get<Player[]>('http://localhost:8000/player_pool').pipe(
      tap(() => console.log('Player pool retrieved!')),
      tap((playerList) => console.log(playerList))
    );
  }

  // get mock draft pool from player list
  getMockDraftPoolFromPlayerList(playerList: Player[]) {
    return {
      qbs: this.getRandomPlayers(
        playerList.filter((p) => p.position === 'QB'),
        this.numQBs
      ),
      rbs: this.getRandomPlayers(
        playerList.filter((p) => p.position === 'RB'),
        this.numRBs
      ),
      wrs: this.getRandomPlayers(
        playerList.filter((p) => p.position === 'WR'),
        this.numWRs
      ),
      tes: this.getRandomPlayers(
        playerList.filter((p) => p.position === 'TE'),
        this.numTEs
      ),
    };
  }

  // return a list of players from the mock player pool, randomly choosing a number of players from each position
  getMockDraftPool() {
    return {
      qbs: this.getRandomPlayers(totalPlayerPool.qbs, this.numQBs),
      rbs: this.getRandomPlayers(totalPlayerPool.rbs, this.numRBs),
      wrs: this.getRandomPlayers(totalPlayerPool.wrs, this.numWRs),
      tes: this.getRandomPlayers(totalPlayerPool.tes, this.numTEs),
    };
  }

  private getRandomPlayers(player_list: Player[], number_to_select: number) {
    let selected_players: Player[] = [];
    while (selected_players.length < number_to_select) {
      const random_index = Math.floor(Math.random() * player_list.length);
      const player = player_list[random_index];
      if (!selected_players.includes(player)) {
        selected_players.push(player);
      }
    }
    return selected_players;
  }

  // calculate stats for player pool.
  // to do this, take each player from the pool and grab their stats from one random game from that season
  // populate the player object's score field with the fantasy points from that game
  // return the updated player pool
  getScoresForPlayerPool(player_pool: PlayerPool) {
    let all_players = [
      ...player_pool.qbs,
      ...player_pool.rbs,
      ...player_pool.wrs,
      ...player_pool.tes,
    ];
    all_players.forEach((player) => {
      //player.score = this.getRandomGame(player).fantasy_points;
      // for now, just generate a random score from 0.0 to 30.0, rounded to 2 decimal places
      player.score = Math.round(Math.random() * 30 * 100) / 100;
    });
  }

  // get scores for roster
  // backend endpoint: @app.get("/season/{season}/player/{player_id}/random_week")
  // async def get_random_week_for_player(season: int, player_id: str) -> PlayerBoxScore:
  getScoresForRoster(roster: Roster) {
    roster.players.forEach((player) => {
      this.http
        .get<PlayerBoxScore>(
          'http://localhost:8000/season/' +
            player.season +
            '/player/' +
            player.id +
            '/random_week'
        )
        .subscribe((playerBoxScore) => {
          console.log(player.name, playerBoxScore.fantasy_points);
          player.score = playerBoxScore.fantasy_points;
        });
    });
  }
}
