import common.api as api
from common.models.fixture import Fixture
from common.models.result import Result
from common.models.league import League
from common.models.stat import Stat
from common.models.user import User
from common.config import config
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def reset_counter():
    logger.info("Resetting API counter...")
    api_call_stat = list(Stat.query("api-call"))[0]
    api_stat_dict = api_call_stat.stat_value.as_dict()
    api_stat_dict["count"] = 0
    api_call_stat.stat_value = api_stat_dict
    api_call_stat.save()


def lambda_handler(event, context):
    reset_counter()

if __name__ == "__main__":
    reset_counter()
