from common.config import config
from common.models.fixture import Fixture
from common.models.result import Result
from common.models.stat import Stat
from common.models.user import User, MapAttribute
import common.api as api
import time
import logging
import configparser
logger = logging.getLogger()
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)


def check_api_limit():
    api_call_stat = list(Stat.query("api-call"))[0]
    api_stat_dict = api_call_stat.stat_value.as_dict()
    logger.info(api_stat_dict)
    logger.info("Current API call count : {}".format(api_stat_dict["count"]))
    return api_stat_dict["count"] < int(config.get("MaxApiCall"))


def check_for_fixture_result():
    
    mu_id = config.get("TeamId")  #Manchester United Team ID

    # Get fixture with status `collected_predictions`
    logger.info("Getting fixture with status `collected_predictions` and current time is 3 hours ahead of start time")
    # check if current time is at least 3 hours ahead of start time of fixture
    fixture_list = list(Fixture.status_index.query("collected_predictions", int(time.time()) - 10800 > Fixture.start_time))

    if(len(fixture_list)) > 0:
        result_dict = None
        f = fixture_list[0]
        if check_api_limit():
            result_dict = api.get_result(f.fixture_id)  # get result
        if result_dict: # if result is found/ game is over
            logger.info("Result for fixture: `{}` found.".format(f.fixture_id))
            logger.info("Score = {}".format(result_dict['score']))
            score = result_dict['score']['fulltime'].strip().replace(" ","").split("-")
            home_goals = int(score[0])
            away_goals = int(score[1])
            scorers = []
            first_goal = 0
            first_card = 0
            for e in result_dict['events']:
                if e['type'].lower() == "goal":
                    if first_goal == 0:
                        first_goal = e['elapsed']
                    if e['team_id'] == int(mu_id):
                        scorers.append(e['player'].split(" ")[-1].lower())

                elif e['type'].lower() == "card" and e['team_id'] == mu_id:
                    if first_card == 0:
                        first_card = e['elapsed']
            
            if home_goals + away_goals != 0:
                result = Result(home_goals=home_goals, away_goals=away_goals, scorers=scorers, first_event=first_goal)
            else:
                result = Result(home_goals=home_goals, away_goals=away_goals, scorers=None, first_event=first_card)
            
            logger.info("Updating result for fixture `{}` and changing status to `updated_result`".format(f.fixture_id))
            f.result = result
            f.status = "updated_result"
            f.save()

def lambda_handler(event, context):
    check_for_fixture_result()

if __name__ == "__main__":
    check_for_fixture_result()
