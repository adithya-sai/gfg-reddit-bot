import logging

from common.models.stat import Stat

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
