import json
import os
import requests

from common.config import config

def get_new_fixtures(team_id):
    url = config["FootballApiBaseUrl"] + "/fixtures/team/" + team_id
    headers = {'X-RapidAPI-Host': config.get("FootballApiHost"), "X-RapidAPI-Key": os.environ["FOOTBALL_API_KEY"]}
    r = requests.get(url, headers=headers)
    rdict = json.loads(r.text)
    return rdict["api"]["fixtures"]

def get_result(fixture_id):
    print(config.get("FootballApiBaseUrl"))
    headers = {'X-RapidAPI-Host': config.get("FootballApiHost"), "X-RapidAPI-Key": os.environ["FOOTBALL_API_KEY"]}
    url = config["FootballApiBaseUrl"] + "/fixtures/id/" + str(fixture_id)
    r = requests.get(url, headers=headers)
    rdict = json.loads(r.text)
    fixture_info = rdict["api"]["fixtures"][0]
    resp = {}
    if fixture_info["statusShort"] == "FT":
        resp['score'] = fixture_info["score"]
        resp['events'] = fixture_info['events']
        resp['home'] = fixture_info['homeTeam']['team_id']
        resp['away'] = fixture_info['awayTeam']['team_id']
    return resp
