import logging

import google_sheets
from common.config import config
from common.models.fixture import Fixture
from common.models.user import User

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def score_users():
    # get fixture with status "updated_result"
    logger.info("Getting fixture with status `updated_result`")
    fixture_list = list(Fixture.status_index.query("updated_result", limit=1))
    if len(fixture_list) > 0:
        f = fixture_list[0]
        logger.info("Calculating users score for the fixture result `{}`".format(f.fixture_id))
        logger.info("Getting predictions for users with fixture_id `{}` in curr_prediction".format(f.fixture_id))

        # get user records where current prediction fixture id is the same as the fixture that ended
        users_list = list(User.scan(User.curr_prediction.fixture == f.fixture_id))
        if len(users_list) > 0:

            user_list_to_save = []
            scoreline_dict = {}
            scorerpoints_dict = {}
            highest_user = None
            for u in users_list:
                u.curr_prediction.points = 0  # just to be sure
                logger.info("Calculating score for user : `{}`".format(u.user_id))
                points = 0
                ur = u.curr_prediction.result

                if ur.scorers:
                    # Calculating scorer points
                    correct_scorers = list()
                    actual_scorers = list(f.result.scorers)
                    logger.info("Correct scorer = {}, pred_scorer = {}".format(actual_scorers, ur.scorers))

                    for s in ur.scorers:
                        if s in actual_scorers:
                            correct_scorers.append(s)
                            actual_scorers.remove(s)

                    scorerpoints_dict[u.user_id] = len(correct_scorers)

                    points = points + len(correct_scorers)
                    logger.info("Adding scorer points, total = {}".format(points))

                if is_correct_result(ur, f.result):
                    points += 2
                    logger.info("Correct result - points = {}".format(points))
                if is_correct_scoreline(ur, f.result):
                    points += 3
                    logger.info("Correct scoreline - points = {}".format(points))
                    scoreline_dict[u.user_id] = 1
                else:
                    # Checking if user predicted more than or equal to 5 goals and result did not have 5 goals
                    if (f.home_team_id == int(config.get("TeamId")) and ur.home_goals >= 5 and len(
                            f.result.scorers) < 5) or (
                            f.away_team_id == int(config.get("TeamId")) and ur.away_goals >= 5 and len(
                            f.result.scorers) < 5):
                        points = points - (len(ur.scorers) - len(correct_scorers))

                # update points
                u = add_points(u, points, f.league)
                user_list_to_save.append(u)

            user_list_to_save = sorted(user_list_to_save, key=lambda x: x.curr_prediction.points, reverse=True)
            for u in user_list_to_save:
                print(u.user_id, u.curr_prediction.points)
            second_list_to_save = []
            highest_user = None
            while user_list_to_save:
                u = user_list_to_save.pop(0)
                if not highest_user:
                    highest_user = u
                else:
                    if u.curr_prediction.points > highest_user.curr_prediction.points:
                        highest_user = u
                    elif u.curr_prediction.points == highest_user.curr_prediction.points:
                        logger.info("{} vs {}".format(u.user_id, highest_user.user_id))
                        if win_tie(u, highest_user, scoreline_dict, scorerpoints_dict, f):
                            logger.info("{} won".format(u.user_id))
                            highest_user = add_points(highest_user, 3, f.league)
                            second_list_to_save.append(highest_user)
                            highest_user = u
                        else:
                            logger.info("Lost to highest user with same points, adding +3")
                            u = add_points(u, 3, f.league)
                            second_list_to_save.append(u)
                    else:
                        # current user less than highest_user, so break
                        second_list_to_save.append(u)
                        break

            highest_user = add_points(highest_user, 5, f.league)
            second_list_to_save.append(highest_user)

            for u in user_list_to_save:
                u.save()
            for u in second_list_to_save:
                u.save()
            return f


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


def win_tie(current_user, highest_user, scoreline_dict, scorerpoints_dict, fixture):
    # check if correct scoreline
    if scoreline_dict.get(current_user.user_id, 0) >= scoreline_dict.get(highest_user.user_id, 0):
        if scoreline_dict.get(current_user.user_id, 0) > scoreline_dict.get(highest_user.user_id, 0):
            return True
        else:
            # if both users have correct scoreline, check scorer points
            if scorerpoints_dict.get(current_user.user_id, 0) > scorerpoints_dict.get(highest_user.user_id, 0):
                return True
            elif scorerpoints_dict.get(current_user.user_id, 0) == scorerpoints_dict.get(highest_user.user_id, 0):
                # if that is also same, check who got the closest first event
                if abs(current_user.curr_prediction.result.first_event - fixture.result.first_event) < \
                        abs(highest_user.curr_prediction.result.first_event - fixture.result.first_event):
                    return True
                elif abs(current_user.curr_prediction.result.first_event - fixture.result.first_event) == \
                        abs(highest_user.curr_prediction.result.first_event - fixture.result.first_event):
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


def lambda_handler(event, context):
    f = score_users()
    if f:
        logger.info("Changing status to `FT` for fixture {}".format(f.fixture_id))
        f.status = "FT"
        # change status to FT
        f.save()
        google_sheets.update_sheets(f)


if __name__ == "__main__":
    f = score_users()
    if f:
        logger.info("Changing status to `FT` for fixture {}".format(f.fixture_id))
        f.status = "FT"
        f.save()
        google_sheets.update_sheets(f)
