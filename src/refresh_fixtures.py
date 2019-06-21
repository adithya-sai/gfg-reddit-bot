import api
from models.fixture import Fixture
from models.result import Result
from models.league import League
from models.user import User

import db


# Get fixtures and update in DB

fixtures_list = api.get_new_fixtures("14")

for f in fixtures_list:
    if f["statusShort"] == "NS" or f["statusShort"] == "TBD":
        new_fixture = Fixture(f["fixture_id"], f["homeTeam"]["team_name"], f["awayTeam"]["team_name"], int(f["event_timestamp"]), f["statusShort"], None, f["league_id"])
        new_fixture.save()