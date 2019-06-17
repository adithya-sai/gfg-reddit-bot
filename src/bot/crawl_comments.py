from db import users_col
from reddit import reddit, MoreComments
from models import Prediction, User, Result
import re

def crawl_predictions(match_id, submission_id):
    submission = reddit.submission(id=submission_id)
    user_predictions = []
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        redditor = top_level_comment.author
        if redditor:
            user = top_level_comment.author.name
            scorers = None
            first_goal = None
            # print("user -> ",top_level_comment.author.name)

            lines = top_level_comment.body.split('\n')
            score_line_re = re.search("([0-9] *- *[0-9])", lines[0])
            if(score_line_re is not None):
                score = score_line_re.group(0).strip().replace(" ","")
                # print("Score -> ", score)
            if(len(lines) > 1):
                for i in range(1, len(lines)):
                    curr_line = lines[i].strip().replace(" ","")
                    if curr_line:
                        scorers = [x.lower() for x in curr_line.split(",")]
                        # print("Scorers - ", scorers)
                        next_index = i+1
                        break
                for i in range(next_index, len(lines)):
                    if lines[i].strip().replace(" ",""):
                        first_goal = lines[i].strip().replace(" ","").replace("\'","")
                        # print("First goal - ", first_goal)
                        break
            # print("----------")
            result = Result(score, scorers, first_goal)
            prediction = Prediction(match_id, result)
            user = User(user, 0, prediction, None, None)
            user_predictions.append(user)
    
    return user_predictions
