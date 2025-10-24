"""Simple Flask app serving Premier League data from SQL Server. For learning."""
from flask import Flask, jsonify, request
from ingest_wrapper import fetch_teams, fetch_players_for_team, fetch_player_stats
from models import Database
import os

app = Flask(__name__)

# Default to pyodbc mssql for VM SQL setup; fallback to sqlite for local dev
DEFAULT_CONN = "mssql+pyodbc://@TTUK02671286934/baller?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
DB_CONN = os.getenv('WEBAPP_DB_CONN', DEFAULT_CONN)
print(f"Using DB connection: {DB_CONN}")

db = Database(DB_CONN)

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all teams."""
    teams = db.get_teams()
    if not teams:
        teams = fetch_teams()
        db.upsert_teams(teams)
        teams = db.get_teams()
    return jsonify(teams)

@app.route('/api/players', methods=['GET'])
def get_players():
    """Get players, optionally filtered by team_id."""
    team_id = request.args.get('team_id')
    if team_id:
        players = db.get_players_by_team(team_id)
        if not players:
            players = fetch_players_for_team(team_id)
            db.upsert_players(players)
            players = db.get_players_by_team(team_id)
    else:
        players = db.get_players()
    return jsonify(players)

@app.route('/api/players/<int:player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    """Get stats for a specific player."""
    stats = fetch_player_stats(player_id)  # get from wrapper
    if not stats:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify(stats)

@app.route('/')
def index():
    """Serve frontend HTML."""
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
