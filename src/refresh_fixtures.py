import common.api as api
from common.models.fixture import Fixture
from common.models.result import Result
from common.models.league import League
from common.models.stat import Stat
from common.models.user import User
from common.config import config
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)


def refresh_fixtures():
	# Get fixtures and update in DB
	logger.info("Refreshing fixtures...")
	api_call_stat = list(Stat.query("api-call"))[0]
	api_stat_dict = api_call_stat.stat_value.as_dict()
	logger.info(api_stat_dict)
	logger.info("Current API call count : {}".format(api_stat_dict["count"]))
	if api_stat_dict["count"] < int(config.get("MaxApiCall")):

		fixtures_list = api.get_new_fixtures(config.get("TeamId"))
		for f in fixtures_list:
			if f["statusShort"] == "NS" or f["statusShort"] == "TBD":
				Fixture(fixture_id=f["fixture_id"], home= f["homeTeam"]["team_name"], away=f["awayTeam"]["team_name"], start_time=int(f["event_timestamp"]), status=f["statusShort"], result=None, league=f["league_id"]).save()
		
		api_stat_dict["count"] += 1
		api_call_stat.stat_value = api_stat_dict
		api_call_stat.save()
	else:
		logger.error("API call limit exceeded. Fixtures not refreshed")


def lambda_handler(event, context):
    refresh_fixtures()

if __name__ == "__main__":
    refresh_fixtures()