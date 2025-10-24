import json, os
import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------
# CONFIG
# -------------------------
DB_CONNECTION   = "mssql+pyodbc://@TTUK02671286934/baller?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
TABLE_NAME      = "Teams" 
# -------------------------
# LOAD JSON
# -------------------------
print("Loading Teams Table.")
with open('teams/teams.json', "r", encoding="utf-8") as f:
    teams = json.load(f)

for team in teams['data']:
    name    = team['name'] 
    id      = team['id']
     

    stadium = team["stadium"]

    # Extract key fields
    record = {
     "TeamId"          : team.get("id")
    ,"Name"            : team.get("name")
    ,"ShortName"       : team.get("shortName")
    ,"abbr"            : team.get("abbr")
    ,"StadiumName"     : stadium.get("name")
    ,"Country"         : stadium.get("country")
    ,"City"            : stadium.get("city")
    ,"Capacity"        : stadium.get("capacity")

    }

    # -------------------------
    # LOAD INTO DATABASE
    # -------------------------
    engine = create_engine(DB_CONNECTION)

    # Create table if not exists (for SQLite demo; for SQL Server, precreate via SQL)
    create_table_sql = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{TABLE_NAME}' AND xtype='U')
    CREATE TABLE {TABLE_NAME} (
         [TeamId]           INT NOT NULL
        ,[Name]             VARCHAR(150) NOT NULL
        ,[ShortName]        VARCHAR(100) NOT NULL
        ,[abbr]             VARCHAR(20) NOT NULL
        ,[StadiumName]      VARCHAR(150) NOT NULL
        ,[Country]          VARCHAR(150) NOT NULL
        ,[City]             VARCHAR(150) NOT NULL
        ,[Capacity]         INT NOT NULL
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))

    # Insert record
    df = pd.DataFrame([record])
    df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False)

    print(f"Successfully loaded \t {id},\t{name}.")