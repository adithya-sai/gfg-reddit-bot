# get fixture by status "posted_thread"
# check if current time > fixture.start_time
# if yes, collect predictions
# change status to "collected_predictions"

from models.fixture import Fixture
from models.submission import Submission
from models.result import Result
from models.user import User, Prediction, Points
import db
import time
import re
import bot
import math

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
            return Result(home_goals, away_goals, scorers, first_event)
    else:
        return None


def collect_predictions():

    fixture_list = db.get_fixtures_by_status("posted_thread")
    if(len(fixture_list)) > 0:

        f = fixture_list[0]
        if time.time() > f['start_time']:
            sub = db.get_submission_by_fixture(f['_id'])
            if sub:
                user_predictions = bot.crawl_predictions(sub.submission_id)
                new_user_list = list()
                for up in user_predictions:
                    
                    lines = up['body'].split('\n')
                    result = extract_result(lines)
                    if result:
                        prediction = Prediction(f['_id'], result, up['posted_at'], 0)

                        existing_user = db.get_user_by_id(up['name'])
                        if not existing_user:
                            # new user
                            new_user = User(up['name'], Points(0, dict()), prediction, list())
                            new_user_list.append(new_user)
                        else:
                            existing_user.prediction_history.append(existing_user.curr_prediction)
                            existing_user.curr_prediction = prediction
                            existing_user.save()

                if len(new_user_list) > 0:
                    db.insert_users_in_bulk(new_user_list)

                fixture = db.get_fixture_by_id(f['_id'])
                if fixture:
                    db.change_fixture_status(fixture, "collected_predictions")
                else:
                    print("fixture not found")
            else:
                print("submission not found")

if __name__ == "__main__":
    collect_predictions()