# get fixture by status "posted_thread"
# check if current time > fixture.start_time
# if yes, collect predictions
# change status to "collected_predictions"

from common.models.fixture import Fixture
from common.models.submission import Submission
from common.models.result import Result
from common.models.user import User, Prediction
import common.bot as bot
import time
import re
import math
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

def extract_result(lines):
    scorers = None
    first_event = None
    score_line_re = re.search("([0-9] *- *[0-9])", lines[0])
    if(score_line_re is not None):
        score = score_line_re.group(0).strip().replace(" ","").split("-")
        home_goals = int(score[0])
        away_goals = int(score[1])
        if(len(lines) > 1):
            for i in range(1, len(lines)):
                curr_line = lines[i].strip().replace(" ","")
                if curr_line:
                    scorers = [x.lower() for x in curr_line.split(",")]
                    next_index = i+1
                    break
            for i in range(next_index, len(lines)):
                if lines[i].strip().replace(" ",""):
                    first_event = lines[i].strip().replace(" ","").replace("\'","")
                    if first_event.isdigit():
                        first_event = int(first_event)
                    else:
                        first_event = 10000         # assigning an insane number if first event is not an integer
                    break
            return Result(home_goals = home_goals, away_goals = away_goals, scorers = scorers, first_event = first_event)
    else:
        return None


def collect_predictions():
    logger.info("Getting fixture with status `posted_thread`")
    fixture_list = list(Fixture.status_index.query("posted_thread", limit = 1))

    if(len(fixture_list)) > 0:
        f = fixture_list[0]
        logger.info("Fixture: {} found. Checking if it started...".format(f.fixture_id))
        if time.time() > f.start_time:
            try:
                logger.info("Fixture {} started. Getting submission for the fixture".format(f.fixture_id))
                sub = list(Submission.fixture_index.query(f.fixture_id))[0]
                logger.info("Type of sub : {}".format(type(sub)))
                logger.info("Submission `{}` found".format(sub.submission_id))
                user_predictions = bot.crawl_predictions(sub.submission_id)
                logger.info("Gathered `{}` user predictions for fixture: {}".format(len(user_predictions), f.fixture_id))
                new_user_list = list()
                for up in user_predictions:
                    
                    lines = up['body'].split('\n')
                    result = extract_result(lines)
                    if result:
                        prediction = Prediction(fixture=f.fixture_id, result = result, posted_at= up['posted_at'], points = 0)
                        existing_user_result = list(User.query(up['name']))
                        if len(existing_user_result) > 0:
                            existing_user = existing_user_result[0]
                            existing_user.prediction_history.append(existing_user.curr_prediction)
                            existing_user.curr_prediction = prediction
                            existing_user.save()
                        else:
                            new_user = User(user_id=up['name'], total_points=0, points_per_league = dict(), curr_prediction=prediction, prediction_history=list())
                            new_user_list.append(new_user)
                        
                if len(new_user_list) > 0:
                    logger.info("Inserting new user predictions of size: {}".format(len(new_user_list)))
                    with User.batch_write() as batch:
                        for u in new_user_list:
                            batch.save(u)

                logger.info("Changing status of fixture from `posted_thread` to `collected_predictions`")
                f.status = "collected_predictions"
                f.save()
            except Exception:
                logging.exception("Error while collecting predictions for fixture:{}".format(f.fixture_id))

    else:
        logger.info("No fixture found with the status `posted_thread`")


def lambda_handler(event, context):
    collect_predictions()

if __name__ == "__main__":
    collect_predictions()