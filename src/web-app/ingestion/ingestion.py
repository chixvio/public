
import requests as re
from helpers import write_file, read_json
import json, time, os


def get_clubs():
    clubs = read_json('clubs.json')
    clubs = json.loads(clubs)
    return clubs



def if __name__ == '__main__':
    clubs = get_clubs()
    get_squad(clubs)
    get_player_stats()

    path = 'teams/squads/'
    club_files = os.listdir(path)
    for file in club_files:
        file_path = path + file
        
        # get players in each file
        with open(file_path, "r", encoding="utf-8") as f:
            squad = json.load(f)
        
        team_id     = squad['team']['id']
        team_name   = squad['team']['name']
        save_path = f"teams/{team_id} - {team_name}"
        os.mkdir(save_path)
        players = squad['players']
        for player in players:
            player_id = player['id']
            player_name = player['name']['display']

            url = f"https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v1/competitions/8/players/{player_id}/stats"
            result = re.get(url)
            data = json.loads(result.text)
            status_code = result.status_code
            print(status_code, player_name)
            if status_code == 200:
                write_file(f"{save_path}/{player_id}.json", data)



def get_squad(clubs):
    for club in clubs:
        club_id     = club['id']
        club_name   = club['name']

        url = f"https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v2/competitions/8/seasons/2025/teams/{club_id}/squad"
        result = re.get(url)
        data = json.loads(result.text)
        status_code = result.status_code
        print(club_name, status_code)
        if status_code == 200:
            write_file(f"club/squad/{club_id}.json", data)
        time.sleep(2)




# clubs = get_clubs()   --> 16/10/2025
# get_squad(clubs)      --> 16/10/2025
get_player_stats()