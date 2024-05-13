import sqlite3

conn = sqlite3.connect('draftduel_test.db')

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
    SELECT *
    FROM players_over_60_points_CTE AS player_pool
    INNER JOIN player_team_and_games_played_CTE AS team_and_games
        ON player_pool.id = team_and_games.id AND player_pool.season = team_and_games.season
    INNER JOIN players AS names
        ON player_pool.id = names.id
    """
).fetchall()

print(len(all_players_points_over_60))
print(all_players_points_over_60)