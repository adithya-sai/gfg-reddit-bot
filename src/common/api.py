import requests
import json
from common.config import config

def get_new_fixtures(team_id):
    url = config["FootballApiBaseUrl"] + "/fixtures/team/" + team_id
    r = requests.get(url)
    rdict = json.loads(r.text)
    return rdict["api"]["fixtures"]

def get_result(fixture_id):
    print(config.get("FootballApiBaseUrl"))

    url = config["FootballApiBaseUrl"]+ "/fixtures/id/" + str(fixture_id)
    r = requests.get(url)
    rdict = json.loads(r.text)
    fixture_info = rdict["api"]["fixtures"][0]
    resp = {}
    if fixture_info["statusShort"] == "FT":
        resp['score'] = fixture_info["score"]
        resp['events'] = fixture_info['events']
    return resp