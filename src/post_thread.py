import datetime
import logging
import time

import common.bot as bot
from common.config import config
from common.models.fixture import Fixture
from common.models.league import League
from common.models.submission import Submission

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Get upcoming fixture.
# check if current time is less than 24 hours away
# make post
# change status to "posted_thread"

def make_reddit_post(f):
    league = League.get(f.league)
    logger.info("Making reddit post for fixture ID: {}, League Name: {}".format(f.fixture_id, league.league_name))
    title = "Going for Gold : {} vs {} [{}]".format(f.home, f.away, league.league_name)
    data = {
        "home": f.home,
        "away": f.away,
        "spreadsheet_link": "https://docs.google.com/spreadsheets/d/" + config.get("SpreadSheetId")
    }
    if f.home_team_id == int(config.get("TeamId")):
        data["s1"] = 2
        data["s2"] = 1
    else:
        data["s2"] = 2
        data["s1"] = 1


    with open('thread_format.txt', 'r') as myfile:
        body = myfile.read().format(**data)

    return bot.submit_post(title, body)


def post_thread():
    try:
        logger.info("Getting the latest fixture")
        fixtures_list = list(Fixture.status_index.query("NS", limit=1))
        if len(fixtures_list) > 0:
            f = fixtures_list[0]
            if f.start_time - int(time.time()) < 86400:
                logger.info("Upcoming fixture : {}".format(f.fixture_id))
                submission = make_reddit_post(f)
                logger.info("Inserting submission - {}, {}".format(submission.id, submission.created_utc))
                Submission(submission_id=submission.id, fixture_id=f.fixture_id,
                           created_at=submission.created_utc).save()
                f.status = "posted_thread"
                logger.info("Changing status of fixture to posted_thread")
                f.save()
            else:
                logger.info("No fixture in the next 24 hours")
        else:
            logger.info("No fixture with status `NS`")

    except Exception:
        logging.exception("Exception occured")


def lambda_handler(event, context):
    post_thread()
    return


if __name__ == "__main__":
    post_thread()
