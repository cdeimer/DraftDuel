import sqlite3
import nfl_data_py as nfl

# Clear the tables in the database
def clear_tables():
    conn = sqlite3.connect('draftduel_test.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM players')
    cursor.execute('DELETE FROM player_seasons')
    cursor.execute('DELETE FROM player_weeks')
    conn.commit()
    conn.close()

# Gather the player data from 2011
def gather_seasonal_data(year: int = 2011):
    season_stats = nfl.import_seasonal_data([year], 'ALL')
    season_stats_filtered = season_stats.filter(['player_id', 'season', 'fantasy_points', 'passing_yards', 'passing_tds', 'interceptions', 'sack_fumbles', 'rushing_yards', 'rushing_tds', 'rushing_fumbles', 'receptions', 'receiving_yards', 'receiving_tds', 'receiving_fumbles'])
    return season_stats_filtered

def add_seasonal_data_to_db():
    season_stats = gather_seasonal_data()
    conn = sqlite3.connect('draftduel_test.db')
    # rename columns to match db schema
    season_stats.rename(columns={'player_id': 'id', 'season': 'season', 'fantasy_points': 'fantasy_points', 'passing_yards': 'pass_yards', 'passing_tds': 'pass_tds', 'interceptions': 'pass_ints', 'sack_fumbles': 'pass_fumbles', 'rushing_yards': 'rush_yards', 'rushing_tds': 'rush_tds', 'rushing_fumbles': 'rush_fumbles', 'receptions': 'rec_recs', 'receiving_yards': 'rec_yards', 'receiving_tds': 'rec_tds', 'receiving_fumbles': 'rec_fumbles'}, inplace=True)
    season_stats.to_sql('player_seasons', conn, if_exists='replace', index=False)
    conn.close()

def gather_weekly_data(year: int = 2011):
    column_list = ['player_id', 'season', 'week', 'recent_team', 'opponent_team', 'fantasy_points', 'passing_yards', 'passing_tds', 'interceptions', 'sack_fumbles', 'rushing_yards', 'rushing_tds', 'rushing_fumbles', 'receptions', 'receiving_yards', 'receiving_tds', 'receiving_fumbles']
    weekly_stats = nfl.import_weekly_data([year], column_list)
    return weekly_stats

def add_weekly_data_to_db():
    weekly_stats = gather_weekly_data()
    conn = sqlite3.connect('draftduel_test.db')
    # rename columns to match db schema
    weekly_stats.rename(columns={'player_id': 'id', 'week': 'week', 'season': 'season', 'recent_team': 'team', 'opponent_team': 'opponent_team', 'fantasy_points': 'fantasy_points', 'passing_yards': 'pass_yards', 'passing_tds': 'pass_tds', 'interceptions': 'pass_ints', 'sack_fumbles': 'pass_fumbles', 'rushing_yards': 'rush_yards', 'rushing_tds': 'rush_tds', 'rushing_fumbles': 'rush_fumbles', 'receptions': 'rec_recs', 'receiving_yards': 'rec_yards', 'receiving_tds': 'rec_tds', 'receiving_fumbles': 'rec_fumbles'}, inplace=True)
    weekly_stats.to_sql('player_weeks', conn, if_exists='replace', index=False)
    conn.close()

def gather_player_data():
    column_list = ['player_id', 'player_name', 'position']
    player_data = nfl.import_seasonal_rosters([2011], column_list)
    return player_data

def add_player_data_to_db():
    player_data = gather_player_data()
    conn = sqlite3.connect('draftduel_test.db')
    # rename columns to match db schema
    player_data.rename(columns={'player_id': 'id', 'player_name': 'name', 'position': 'position'}, inplace=True)
    player_data.to_sql('players', conn, if_exists='replace', index=False)
    conn.close()

def test_imports():
    print(nfl.import_weekly_data([2011]).columns)
    # print(nfl.import_ids().columns)
    # column_list = ['gsis_id', 'name', 'position', 'team', 'birthdate', 'draft_year']
    # print(nfl.import_ids().sample(10).filter(column_list))

add_weekly_data_to_db()
add_seasonal_data_to_db()
add_player_data_to_db()

# ['player_id', 'season', 'fantasy_points', 'passing_yards', 'passing_tds', 'interceptions', 'sack_fumbles', 'rushing_yards', 'rushing_tds', 'rushing_fumbles', 'receptions', 'receiving_yards', 'receiving_tds', 'receiving_fumbles']