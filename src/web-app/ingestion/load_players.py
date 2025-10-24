import json, os
import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------
# CONFIG
# -------------------------
DB_CONNECTION   = "mssql+pyodbc://@TTUK02671286934/baller?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
TABLE_NAME      = "Players"
# -------------------------
# LOAD JSON
# -------------------------
path = 'teams/'
TEAMS = os.listdir(path)
print(TEAMS)

for team in TEAMS:

    player_files = os.listdir(path + '/' + team)

    for file in player_files:
        NEW_PATH = path + '/' + team + '/' + file
        file_path = path + file
            
        with open(NEW_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        _player     = data["player"]
        _country    = _player['country'] 
        id          = _player['id']
        name        = _player['name']
        position    = _player['position']
        firstName   = _player['firstName']     
        lastName    = _player['lastName']          
        isoCode     = _country['isoCode']     
        country     = _country['country']          
        demonym     = _country['demonym']          

        # Extract key fields
        record = {
            "PlayerId"      : id,   
            "name"          : name,   
            "position"      : position,       
            "firstName"     : firstName,       
            "lastName"      : lastName,       
            "isoCode"       : isoCode,       
            "country"       : country,       
            "demonym"       : demonym       
        }

        # -------------------------
        # LOAD INTO DATABASE
        # -------------------------
        engine = create_engine(DB_CONNECTION)

        # Create table if not exists (for SQLite demo; for SQL Server, precreate via SQL)
        create_table_sql = f"""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{TABLE_NAME}' AND xtype='U')
        CREATE TABLE {TABLE_NAME} (
            [PlayerId]     INT NOT NULL
            ,[name]         VARCHAR(100) NOT NULL
            ,[position]     VARCHAR(100) NOT NULL
            ,[firstName]    VARCHAR(100) NOT NULL
            ,[lastName]     VARCHAR(100) NOT NULL
            ,[isoCode]      VARCHAR(20)  NULL
            ,[country]      VARCHAR(100) NULL
            ,[demonym]      VARCHAR(100) NULL

        );
        """
        with engine.begin() as conn:
            conn.execute(text(create_table_sql))

        # Insert record
        df = pd.DataFrame([record])
        df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False)

        print(f"Successfully loaded \t {id},\t{name}.")