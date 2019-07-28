import logging

from praw.models import MoreComments

from common.config import config
from common.reddit import reddit

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def crawl_predictions(submission_id):
    logger.info("Calling reddit API to get submission: {}".format(submission_id))
    submission = reddit.submission(id=submission_id)
    user_predictions = []
    user_set = set()
    submission.comments.replace_more(limit=None)
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            logger.info("more comments found")
            continue
        redditor = top_level_comment.author
        if redditor:
            if top_level_comment.author.name not in user_set:
                user_predictions.append({'name': top_level_comment.author.name, 'body': top_level_comment.body,
                                         'posted_at': top_level_comment.created_utc})
                user_set.add(top_level_comment.author.name)
    return user_predictions


def submit_post(title, body):
    subreddit = reddit.subreddit(config.get('Subreddit'))
    submission = subreddit.submit(title, body)
    return submission
