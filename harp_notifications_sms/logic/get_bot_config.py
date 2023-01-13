import requests
from logger.logging import service_logger
import harp_notifications_sms.settings as settings
import traceback

logger = service_logger()


def bot_config(bot_name):
    url = f"{settings.BOTS_SERVICE}/{bot_name}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    logger.info(msg=f"Request {bot_name} config from bots service: {url}")
    try:
        req = requests.get(url=url, headers=headers, timeout=10, verify=False)
        if req.status_code == 200:
            logger.info(msg=f"Receive {bot_name} response from bots service: {req.json()}")
            return req.json()['config']
        else:
            logger.error(msg=f"Error during receiving bot config: {req.content}, stack: {traceback.format_exc()}")
    except Exception as err:
        logger.error(msg=f"Error during receiving bot config: {err}, stack: {traceback.format_exc()}")
        return {'msg': None}
