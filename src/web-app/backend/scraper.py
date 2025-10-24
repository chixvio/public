"""
Very small scraper module that targets a public football data API.
This is written for learning: calls are minimal and responses are normalized.

Assumptions:
- There's an open API endpoint serving teams, players, fixtures. If not, replace URLs with your API keys/endpoints.
- The scraper uses requests and handles simple retries.
"""
import requests
import time

BASE = 'https://api.football-data.org/v2'  # example public API; requires X-Auth-Token for some endpoints

class PremierScraper:
    def __init__(self, token=None):
        self.token = token or ''
        self.headers = {'X-Auth-Token': self.token} if self.token else {}

    def _get(self, path, params=None):
        url = f"{BASE}{path}"
        for attempt in range(3):
            try:
                r = requests.get(url, params=params, headers=self.headers, timeout=10)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                time.sleep(1)
                last = e
        raise last

    def fetch_teams(self):
        # For EPL: competitions/PL/teams
        data = self._get('/competitions/PL/teams')
        teams = []
        for t in data.get('teams', []):
            teams.append({
                'external_id': t.get('id'),
                'name': t.get('name'),
                'shortName': t.get('shortName'),
                'tla': t.get('tla'),
                'venue': t.get('venue')
            })
        return teams

    def fetch_all_players(self):
        # football-data.org doesn't provide all players at once; iterate over teams
        teams = self.fetch_teams()
        players = []
        for t in teams:
            team_id = t['external_id']
            try:
                data = self._get(f'/teams/{team_id}')
                for p in data.get('squad', []):
                    players.append({
                        'external_id': p.get('id'),
                        'name': p.get('name'),
                        'position': p.get('position'),
                        'nationality': p.get('nationality'),
                        'dateOfBirth': p.get('dateOfBirth')
                    })
            except Exception:
                continue
        return players

    def fetch_fixtures(self):
        # Sample: get matches for competition
        data = self._get('/competitions/PL/matches')
        fixtures = []
        for m in data.get('matches', []):
            fixtures.append({
                'external_id': m.get('id'),
                'utcDate': m.get('utcDate'),
                'status': m.get('status'),
                'matchday': m.get('matchday'),
                'homeTeam': m.get('homeTeam', {}).get('id'),
                'awayTeam': m.get('awayTeam', {}).get('id')
            })
        return fixtures
