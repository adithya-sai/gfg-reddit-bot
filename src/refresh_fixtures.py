import logging

import common.api as api
from common.config import config
from common.models.fixture import Fixture
from common.models.stat import Stat

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def refresh_fixtures():
    # Get fixtures and update in DB
    logger.info("Refreshing fixtures...")
    api_call_stat = list(Stat.query("api-call"))[0]
    api_stat_dict = api_call_stat.stat_value.as_dict()
    available_leagues = list(Stat.query("available_leagues"))[0].stat_value.as_dict()["curr"]
    logger.info(api_stat_dict)
    logger.info("Current API call count : {}".format(api_stat_dict["count"]))
    if api_stat_dict["count"] < int(config.get("MaxApiCall")):

        fixtures_list = api.get_new_fixtures(config.get("TeamId"))
        for f in fixtures_list:
            if (f["statusShort"] == "NS" or f["statusShort"] == "TBD") and f["league_id"] in available_leagues:
                Fixture(fixture_id=f["fixture_id"], home=f["homeTeam"]["team_name"], away=f["awayTeam"]["team_name"],
                        home_team_id=f['homeTeam']['team_id'], away_team_id=f['awayTeam']['team_id'],
                        start_time=int(f["event_timestamp"]), status=f["statusShort"], result=None,
                        league=f["league_id"]).save()

        api_stat_dict["count"] += 1
        api_call_stat.stat_value = api_stat_dict
        api_call_stat.save()
    else:
        logger.error("API call limit exceeded. Fixtures not refreshed")


def lambda_handler(event, context):
    refresh_fixtures()


if __name__ == "__main__":
    refresh_fixtures()
