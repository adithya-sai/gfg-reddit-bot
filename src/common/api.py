import requests
import json

def get_new_fixtures(team_id):
    url = "https://www.api-football.com/demo/api/v2/fixtures/team/" + team_id
    r = requests.get(url)
    rdict = json.loads(r.text)
    return rdict["api"]["fixtures"]

def get_result(fixture_id):
    url = "https://www.api-football.com/demo/api/v2/fixtures/id/" + str(fixture_id)
    r = requests.get(url)
    rdict = json.loads(r.text)
    fixture_info = rdict["api"]["fixtures"][0]
    resp = {}
    if fixture_info["statusShort"] == "FT":
        resp['score'] = fixture_info["score"]
        resp['events'] = fixture_info['events']
    return resp