"""
Simple DB layer that matches the schema from load_teams.py and load_players.py.
Handles only Teams and Players tables initially - those are core tables we need.
Uses SQLAlchemy for portability between SQLite (dev) and SQL Server (prod).
"""
from sqlalchemy import (create_engine, Column, Integer, String, Table, MetaData, DateTime)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select, text
import datetime

class Database:
    def __init__(self, conn_string='sqlite:///data.db'):
        self.engine = create_engine(conn_string, echo=False, future=True)
        self.meta = MetaData()
        
        # Teams table matching load_teams.py schema
        self.teams = Table('Teams', self.meta,
            Column('TeamId', Integer, primary_key=True),
            Column('Name', String(150), nullable=False),
            Column('ShortName', String(100), nullable=False),
            Column('abbr', String(20), nullable=False),
            Column('StadiumName', String(150), nullable=False),
            Column('Country', String(150), nullable=False),
            Column('City', String(150), nullable=False),
            Column('Capacity', Integer, nullable=False)
        )

        # Players table matching load_players.py schema
        self.players = Table('Players', self.meta,
            Column('PlayerId', Integer, primary_key=True),
            Column('name', String(100), nullable=False),
            Column('position', String(100), nullable=False),
            Column('firstName', String(100), nullable=False),
            Column('lastName', String(100), nullable=False),
            Column('isoCode', String(20)),
            Column('country', String(100)),
            Column('demonym', String(100))
        )

        # Create tables if they don't exist
        self.meta.create_all(self.engine)

    def upsert_teams(self, teams_list):
        """Insert or update teams. Note: team_id is the natural key."""
        with self.engine.begin() as conn:
            for t in teams_list:
                # Find by TeamId (natural key from Premier League API)
                stmt = select(self.teams.c.TeamId).where(self.teams.c.TeamId == t['TeamId'])
                res = conn.execute(stmt).fetchone()
                
                # Map fields to match the schema from load_teams.py
                team_data = {
                    'TeamId': t.get('TeamId'),
                    'Name': t.get('Name'),
                    'ShortName': t.get('ShortName'),
                    'abbr': t.get('abbr'),
                    'StadiumName': t.get('StadiumName', 'Unknown'),
                    'Country': t.get('Country', 'England'),  # default for Premier League
                    'City': t.get('City', 'Unknown'),
                    'Capacity': t.get('Capacity', 0)
                }
                
                if res:
                    # Update existing
                    conn.execute(
                        self.teams.update()
                        .where(self.teams.c.TeamId == t['TeamId'])
                        .values(**team_data)
                    )
                else:
                    try:
                        # Insert new
                        conn.execute(self.teams.insert().values(**team_data))
                    except IntegrityError:
                        pass  # already exists

    def get_teams(self):
        """Get all teams."""
        with self.engine.connect() as conn:
            res = conn.execute(select(self.teams)).mappings().all()
            return [dict(r) for r in res]

    def upsert_players(self, players_list):
        """Insert or update players. Note: PlayerId is the natural key."""
        with self.engine.begin() as conn:
            for p in players_list:
                # Find by PlayerId (natural key from Premier League API)
                stmt = select(self.players.c.PlayerId).where(self.players.c.PlayerId == p['PlayerId'])
                res = conn.execute(stmt).fetchone()
                
                # Map fields to match the schema from load_players.py
                player_data = {
                    'PlayerId': p.get('PlayerId'),
                    'name': p.get('name'),
                    'position': p.get('position'),
                    'firstName': p.get('firstName'),
                    'lastName': p.get('lastName', ''),
                    'isoCode': p.get('isoCode'),
                    'country': p.get('country'),
                    'demonym': p.get('demonym')
                }
                
                if res:
                    # Update existing
                    conn.execute(
                        self.players.update()
                        .where(self.players.c.PlayerId == p['PlayerId'])
                        .values(**player_data)
                    )
                else:
                    try:
                        # Insert new
                        conn.execute(self.players.insert().values(**player_data))
                    except IntegrityError:
                        pass

    def get_players(self):
        """Get all players."""
        with self.engine.connect() as conn:
            res = conn.execute(select(self.players)).mappings().all()
            return [dict(r) for r in res]

    def get_players_by_team(self, team_id):
        """Get players filtered by team. Note: this requires PlayerClubs table 
        which we don't have yet. For now returns all players."""
        return self.get_players()
