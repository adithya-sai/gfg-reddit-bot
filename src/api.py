import requests
import json
from models.fixture import Fixture

def get_new_fixtures(team_id):
    url = "https://www.api-football.com/demo/api/v2/fixtures/team/" + team_id
    r = requests.get(url)
    rdict = json.loads(r.text)
    return rdict["api"]["fixtures"]