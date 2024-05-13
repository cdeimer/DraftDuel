from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    # Add other origins as needed
]

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class Player(BaseModel):
    id: str
    name: str
    position: str
    season: int
    team: str
    fantasy_points: float
    games_played: int


class PlayerBoxScore(BaseModel):
    week: int
    team: str
    opponent: str
    fantasy_points: float
    pass_yards: int
    pass_tds: int
    pass_ints: int
    pass_fumbles: int
    rush_yards: int
    rush_tds: int
    rush_fumbles: int
    rec_recs: int
    rec_yards: int
    rec_tds: int
    rec_fumbles: int

@app.get("/")
async def root():
    return {"message": "API is running!"}

@app.get("/player_pool")
async def get_player_pool() -> list[Player]:
    conn = sqlite3.connect('../database/draftduel_test.db')
    cur = conn.cursor()
    all_players_points_over_60 = cur.execute(
        """
        WITH players_over_60_points_CTE AS (
            SELECT
                id,
                season,
                fantasy_points
            FROM player_seasons
            WHERE fantasy_points > 60
        ),
        player_team_and_games_played_CTE AS (
            SELECT
                id,
                season,
                MAX(team) AS team,
                COUNT(team) AS games_played
            FROM player_weeks
            GROUP BY id, season
        )
        SELECT player_pool.id, names.name, names.position, player_pool.season, team_and_games.team, player_pool.fantasy_points, team_and_games.games_played    
        FROM players_over_60_points_CTE AS player_pool
        INNER JOIN player_team_and_games_played_CTE AS team_and_games
            ON player_pool.id = team_and_games.id AND player_pool.season = team_and_games.season
        INNER JOIN players AS names
            ON player_pool.id = names.id
        """
    ).fetchall()

    player_pool = []
    for player in all_players_points_over_60:
        player_pool.append(Player(id=player[0], name=player[1], position=player[2], season=player[3], team=player[4], fantasy_points=player[5], games_played=player[6]))
    return player_pool

@app.get("/season/{season}/player/{player_id}/random_week")
async def get_random_week_for_player(season: int, player_id: str) -> PlayerBoxScore:
    conn = sqlite3.connect('../database/draftduel_test.db')
    cur = conn.cursor()
    player_weeks = cur.execute(
        """
        SELECT
            week,
            team,
            opponent_team,
            fantasy_points,
            pass_yards,
            pass_tds,
            pass_ints,
            pass_fumbles,
            rush_yards,
            rush_tds,
            rush_fumbles,
            rec_recs,
            rec_yards,
            rec_tds,
            rec_fumbles
        FROM player_weeks
        WHERE id = ? AND season = ?
        ORDER BY RANDOM()
        LIMIT 1
        """,
        (player_id, season)
    ).fetchall()

    return PlayerBoxScore(
        week=player_weeks[0][0],
        team=player_weeks[0][1],
        opponent=player_weeks[0][2],
        fantasy_points=player_weeks[0][3],
        pass_yards=player_weeks[0][4],
        pass_tds=player_weeks[0][5],
        pass_ints=player_weeks[0][6],
        pass_fumbles=player_weeks[0][7],
        rush_yards=player_weeks[0][8],
        rush_tds=player_weeks[0][9],
        rush_fumbles=player_weeks[0][10],
        rec_recs=player_weeks[0][11],
        rec_yards=player_weeks[0][12],
        rec_tds=player_weeks[0][13],
        rec_fumbles=player_weeks[0][14]
    )

