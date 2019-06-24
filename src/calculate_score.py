# get fixture with status "collected_predictions"
# check if current time is at least 3 hours ahead of start_time
# if yes, call football api to get the result
# get user records where current prediction fixture id is the same as the fixture that ended
# calculate scores for those users and update them on db
# change status to FT

import time
import re
from common.models.fixture import Fixture
from common.models.result import Result
from common.models.user import User, MapAttribute
import common.api as api
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

mu_id = 14      #Manchester United Team ID


def score_users(f):
    logger.info("Calculating users score for the fixture result `{}`".format(f.fixture_id))
    logger.info("Getting predictions for users with fixture_id `{}` in curr_prediction".format(f.fixture_id))

    users_list = list(User.scan(User.curr_prediction.fixture == f.fixture_id))
    print(users_list)
    if len(users_list) > 0:
        highest_user = None
        highest_user_info = {}
        for u in users_list:
            current_user_info = {'scoreline': 0, 'scorers_points': 0}
            points = 0
            ur = u.curr_prediction.result
            if is_correct_result(ur, f.result):
                points += 2
            if is_correct_scoreline(ur, f.result):
                points += 3
                current_user_info['scoreline'] = 1
            correct_scorers = list()
            actual_scorers = f.result.scorers
            for s in ur.scorers:
                if s in actual_scorers:
                    correct_scorers.append(s)
                    actual_scorers.remove(s)
            
            points = points + len(correct_scorers)
            current_user_info['scorers_points'] = len(correct_scorers)

            # update points
            u = add_points(u, points, f.league)
            u.save()

            if highest_user:
                if points > highest_user.curr_prediction.points:
                    highest_user = u
                elif points == highest_user.curr_prediction.points:
                    if win_tie(u, current_user_info, highest_user, highest_user_info, f):
                        add_points(highest_user, 3, f.league)
                        highest_user = u
                        highest_user_info = current_user_info
                    else:
                        add_points(u, 3, f.league)
            else:
                highest_user = u
                highest_user_info = current_user_info

        add_points(highest_user, 5, f.league)

def is_correct_result(ur, fixture_result):
    actual_result_diff = fixture_result.home_goals - fixture_result.away_goals
    user_result_diff = ur.home_goals - ur.away_goals
    if actual_result_diff < 0 and user_result_diff < 0:
        return True
    elif actual_result_diff > 0 and user_result_diff > 0:
        return True
    elif actual_result_diff == user_result_diff:
        return True
    else:
        return False

def is_correct_scoreline(ur, fixture_result):
    if ur.home_goals == fixture_result.home_goals and ur.away_goals == fixture_result.away_goals:
        return True

def win_tie(current_user, current_user_info, highest_user, highest_user_info, fixture):
    # check if correct scoreline
    if current_user_info['scoreline'] >= highest_user_info['scoreline']:
        if current_user_info['scoreline'] > highest_user_info['scoreline']:
            return True
        else:
            # if both users have correct scoreline, check scorer points
            if current_user_info['scorers_points'] > highest_user_info['scorer_points']:
                return True
            elif current_user_info['scorer_points'] == highest_user_info['scorer_points']:
                # if that is also same, check who got the closest first event
                if abs(current_user.result.first_event - fixture.result.first_event) < \
                    abs(highest_user.result.first_event - fixture.result.first_event):
                    return True
                elif abs(current_user.result.first_event - fixture.result.first_event) == \
                    abs(highest_user.result.first_event - fixture.result.first_event):
                    return current_user.curr_prediction.posted_at < highest_user.curr_prediction.posted_at
    else:
        return False

def add_points(u, points, league_id):
    u.curr_prediction.points += points
    u.total_points += points
    ppl_dict = u.points_per_league.as_dict()
    if ppl_dict.get(str(league_id)):
        ppl_dict[str(league_id)] += points
    else:
        ppl_dict[str(league_id)] = points
    u.points_per_league = ppl_dict
    return u


def check_for_fixture_result():
    # Get fixture with status `collected_predictions`
    logger.info("Getting fixture with status `collected_predictions` and current time is 3 hours ahead of start time")
    # check if current time is at least 3 hours ahead of start time of fixture
    fixture_list = list(Fixture.status_index.query("collected_predictions", int(time.time()) - 10800 > Fixture.start_time))

    if(len(fixture_list)) > 0:
        f = fixture_list[0]
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
                    if e['team_id'] == mu_id:
                        scorers.append(e['player'].split(" ")[-1].lower())

                elif e['type'].lower() == "card" and e['team_id'] == mu_id:
                    if first_card == 0:
                        first_card = e['elapsed']
            
            if home_goals + away_goals != 0:
                result = Result(home_goals=home_goals, away_goals=away_goals, scorers=scorers, first_event=first_goal)
            else:
                result = Result(home_goals=home_goals, away_goals=away_goals, scorers=None, first_event=first_card)
            
            logger.info("Updating result for fixture `{}` and changing status to `FT`".format(f.fixture_id))
            f.result = result
            return f


def lambda_handler(event, context):
    f = check_for_fixture_result()
    if f:
        score_users(f)
        logger.info("Changing status to `FT` for fixture {}".format(f.fixture_id))
        f.status = "FT"
        f.save()


if __name__ == "__main__":
    f = check_for_fixture_result()
    if f:
        score_users(f)
        logger.info("Changing status to `FT` for fixture {}".format(f.fixture_id))
        f.status = "FT"
        f.save()
