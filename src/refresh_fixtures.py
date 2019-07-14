import common.api as api
from common.models.fixture import Fixture
from common.models.result import Result
from common.models.league import League
from common.models.user import User
from common.config import config


# Get fixtures and update in DB

fixtures_list = api.get_new_fixtures(config.get("TeamId"))

for f in fixtures_list:
    if f["statusShort"] == "NS" or f["statusShort"] == "TBD":
        Fixture(fixture_id=f["fixture_id"], home= f["homeTeam"]["team_name"], away=f["awayTeam"]["team_name"], start_time=int(f["event_timestamp"]), status=f["statusShort"], result=None, league=f["league_id"]).save()