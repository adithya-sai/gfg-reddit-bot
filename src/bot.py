from models.result import Result
from models.user import User, Prediction
from models.submission import Submission
from reddit import reddit, MoreComments
import re


def crawl_predictions(submission_id):
    submission = reddit.submission(id=submission_id)
    user_predictions = []
    user_set = set()
    for top_level_comment in submission.comments:
        print("test")
        if isinstance(top_level_comment, MoreComments):
            continue
        redditor = top_level_comment.author
        if redditor:
            if top_level_comment.author.name not in user_set:
                user_predictions.append({'name':top_level_comment.author.name, 'body': top_level_comment.body, 'posted_at': top_level_comment.created_utc})
                user_set.add(top_level_comment.author.name)    
    return user_predictions


def submit_post(title, body):
    subreddit = reddit.subreddit('testingground4bots')
    submission = subreddit.submit(title, body)
    return submission