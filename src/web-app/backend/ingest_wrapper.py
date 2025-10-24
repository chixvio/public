"""Small wrapper around ingestion scripts to fetch Premier League data."""
import sys, os, json
from pathlib import Path

# Add ingestion dir to path so we can import scripts
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.append(str(ROOT_DIR / 'ingestion'))

# Now we can import ingestion modules
from ingestion import get_clubs, get_squad, get_player_stats

def fetch_teams():
    """Fetch teams data from Premier League API."""
    clubs = get_clubs()
    return clubs

def fetch_players_for_team(team_id):
    """Fetch players for a specific team."""
    clubs = get_clubs()
    club = next((c for c in clubs if c['id'] == team_id), None)
    if not club:
        return []
    get_squad([club])  # get_squad expects a list
    squad_path = f"club/squad/{team_id}.json"
    if os.path.exists(squad_path):
        with open(squad_path, 'r') as f:
            return json.load(f)
    return []

def fetch_player_stats(player_id):
    """Fetch stats for a specific player."""
    get_player_stats()  # this will fetch all players
    # find player file in teams/<team_id> - <team_name>/<player_id>.json
    for team_dir in os.listdir('teams'):
        if not team_dir.startswith('.'):  # skip . files
            player_file = f"teams/{team_dir}/{player_id}.json"
            if os.path.exists(player_file):
                with open(player_file, 'r') as f:
                    return json.load(f)
    return None