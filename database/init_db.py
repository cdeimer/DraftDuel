import sqlite3

# Define your SQL schema
schema = """

DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS player_seasons;
DROP TABLE IF EXISTS player_weeks;

CREATE TABLE players (
  id TEXT PRIMARY KEY,
  name TEXT,
  position TEXT
);

CREATE TABLE player_seasons (
  id TEXT,
  season INTEGER,
  fantasy_points REAL,
  pass_yards INTEGER,
  pass_tds INTEGER,
  pass_ints INTEGER,
  pass_fumbles INTEGER,
  rush_yards INTEGER,
  rush_tds INTEGER,
  rush_fumbles INTEGER,
  rec_recs INTEGER,
  rec_yards INTEGER,
  rec_tds INTEGER,
  rec_fumbles INTEGER,
  PRIMARY KEY (id, season),
  FOREIGN KEY (id) REFERENCES players (id)
);
CREATE INDEX idx_player_seasons_season ON player_seasons(season);

CREATE TABLE player_weeks (
  id TEXT,
  season INTEGER,
  week INTEGER,
  team TEXT,
  opponent_team TEXT,
  fantasy_points REAL,
  pass_yards INTEGER,
  pass_tds INTEGER,
  pass_ints INTEGER,
  pass_fumbles INTEGER,
  rush_yards INTEGER,
  rush_tds INTEGER,
  rush_fumbles INTEGER,
  rec_recs INTEGER,
  rec_yards INTEGER,
  rec_tds INTEGER,
  rec_fumbles INTEGER,
  PRIMARY KEY (id, season, week),
  FOREIGN KEY (id) REFERENCES players (id)
);
CREATE INDEX idx_player_weeks_season_week ON player_weeks(season, week);
"""

# Connect to the SQLite database
conn = sqlite3.connect('draftduel_test.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Executing the schema
cursor.executescript(schema)

# Commit your changes in the database
conn.commit()

# Close the connection
conn.close()
