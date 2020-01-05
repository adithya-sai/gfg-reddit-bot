# get fixture by status "posted_thread"
# check if current time > fixture.start_time
# if yes, collect predictions
# change status to "collected_predictions"

import logging
import re
import time

import common.bot as bot
from common.config import config
from common.models.fixture import Fixture
from common.models.result import Result
from common.models.submission import Submission
from common.models.user import User, Prediction

logger = logging.getLogger()
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.INFO)


def extract_result(lines, fixture):
    scorers = None
    first_event = 10000 # initialize - assigning an insane number
    score_line_re = re.search("([0-9] *- *[0-9])", lines[0])
    if score_line_re is not None:
        score = score_line_re.group(0).strip().replace(" ", "").split("-")
        home_goals = int(score[0])
        away_goals = int(score[1])
        if len(lines) > 1:
            next_index = 1
            if (fixture.home_team_id == int(config.get("TeamId")) and home_goals != 0) or (
                    fixture.away_team_id == int(config.get("TeamId")) and away_goals != 0):
                for i in range(next_index, len(lines)):
                    curr_line = lines[i].strip().replace(" ", "")
                    if curr_line and "&#" not in curr_line:
                        scorers = [x.lower() for x in curr_line.split(",")]
                        logger.info("Scorers: {}".format(scorers))
                        if fixture.home_team_id == int(config.get("TeamId")):
                            scorers = scorers[0:home_goals]
                        else:
                            scorers = scorers[0:away_goals]
                        scorers = list(filter(None, scorers))
                        next_index = i + 1
                        break
            for i in range(next_index, len(lines)):
                if lines[i].strip().replace(" ", ""):
                    first_event_re = re.search("[0-9]{1,2}", lines[i])
                    if first_event_re:
                        if first_event_re.group(0).isdigit():
                            first_event = int(first_event_re.group(0))
                            logger.info("First event = {}".format(first_event))
                        break
            return Result(home_goals=home_goals, away_goals=away_goals, home_team_id=fixture.home_team_id,
                          away_team_id=fixture.away_team_id, scorers=scorers, first_event=first_event)
    else:
        return None


def collect_predictions():
    logger.info("Getting fixture with status `posted_thread`")
    fixture_list = list(Fixture.status_index.query("posted_thread", limit=1))

    if (len(fixture_list)) > 0:
        f = fixture_list[0]
        logger.info("Fixture: {} found. Checking if it started...".format(f.fixture_id))
        if time.time() > f.start_time:
            try:
                logger.info("Fixture {} started. Getting submission for the fixture".format(f.fixture_id))
                sub = list(Submission.fixture_index.query(f.fixture_id))[0]
                logger.info("Type of sub : {}".format(type(sub)))
                logger.info("Submission `{}` found".format(sub.submission_id))
                user_predictions = bot.crawl_predictions(sub.submission_id)
                logger.info(
                    "Gathered `{}` user predictions for fixture: {}".format(len(user_predictions), f.fixture_id))
                new_user_list = list()
                user_set = set()
                for up in user_predictions:
                    lines = up['body'].split('\n')
                    logger.info("Current user : {}. Lines : {}".format(up["name"],lines))
                    result = extract_result(lines, f)
                    if result and up['name'] not in user_set:
                        prediction = Prediction(fixture=f.fixture_id, result=result, posted_at=up['posted_at'],
                                                points=0)
                        existing_user_result = list(User.query(up['name']))
                        if len(existing_user_result) > 0:
                            logger.info("User : {} is an existing user".format(up["name"]))
                            existing_user = existing_user_result[0]
                            existing_user.curr_prediction = prediction
                            existing_user.save()
                        else:
                            logger.info("User : {} is a new user".format(up["name"]))
                            new_user = User(user_id=up['name'], total_points=0, points_per_league=dict(),
                                            curr_prediction=prediction)
                            new_user_list.append(new_user)
                        user_set.add(up['name'])

                if len(new_user_list) > 0:
                    logger.info("Inserting new user predictions of size: {}".format(len(new_user_list)))
                    for u in new_user_list:
                        u.save()

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
