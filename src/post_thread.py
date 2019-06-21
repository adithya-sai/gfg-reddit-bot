import time
import datetime
import db
import bot
from models.fixture import Fixture
from models.result import Result
from models.league import League
from models.user import User
from models.submission import Submission

# Get upcoming fixture
# check if current time is less than 24 hours away
# make post
# change status to "posted_thread"

def make_reddit_post(f):
    title = "Going for Gold : {} vs {} [{}]".format(f.home, f.away, f.league.league_name)
    data = {
        "home": f.home,
        "away": f.away,
        "start_time": datetime.datetime.utcfromtimestamp(f.start_time)
    }

    with open('thread_format.txt', 'r') as myfile:
        body = myfile.read().format(**data)
    
    return bot.submit_post(title, body)


def post_thread():

    fixtures_list = db.get_fixtures_by_status("NS")
    if len(fixtures_list) > 0:
        fixture_dict = fixtures_list[0]
        if fixture_dict['start_time'] - int(time.time()) < 86400:
            
            f = db.get_fixture_by_id(fixture_dict['_id'])
            submission = make_reddit_post(f)
            db.save_submission(submission.id, f.fixture_id, submission.created_utc)
            db.change_fixture_status(f, "posted_thread")

if __name__ == "__main__":
    post_thread()