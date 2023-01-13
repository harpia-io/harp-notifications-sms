from twilio.rest import Client
import datetime
from logger.logging import service_logger
from harp_notifications_sms.metrics.service_monitoring import Prom
from harp_notifications_sms.logic.get_bot_config import bot_config

logger = service_logger()


class SMSNotifications(object):
    def __init__(self, twilio_account_sid, twilio_auth_token, twilio_phone_number):
        self.twilio_account_sid = twilio_account_sid
        self.twilio_auth_token = twilio_auth_token
        self.twilio_phone_number = twilio_phone_number
        self.bot_config = self.get_bot_config()
        self.client = Client(self.bot_config['TWILIO_ACCOUNT_SID'], self.bot_config['TWILIO_AUTH_TOKEN'])

    def get_bot_config(self):
        if self.twilio_account_sid:
            config = {
                'TWILIO_ACCOUNT_SID': self.twilio_account_sid,
                'TWILIO_AUTH_TOKEN': self.twilio_auth_token,
                'TWILIO_PHONE_NUMBER': self.twilio_phone_number
            }
        else:
            config = bot_config(bot_name='sms')

        return config

    def check_status(self, sid):
        message = self.client.messages.get(sid=sid).fetch()

        status = {
            'sid': message.sid,
            'error_code': message.error_code,
            'error_message': message.error_message,
            'status': message.status,
            'price': message.price,
            'price_unit': message.price_unit
        }

        return status

    @staticmethod
    def convert_time(timestamp):
        converted_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        return converted_time

    @Prom.SEND_SMS_NOTIFICATION.time()
    def create_notification(self, to_number: str, body: str):

        logger.info(msg=f"String to send: {body}")

        message = self.client.messages.create(
                             body=body,
                             from_=self.bot_config['TWILIO_PHONE_NUMBER'],
                             to=to_number
                         )

        status = {
            'sid': message.sid,
            'error_code': message.error_code,
            'error_message': message.error_message,
            'status': message.status,
            'price': message.price,
            'price_unit': message.price_unit
        }

        logger.info(msg=f"Person received the sms: {status}")

        return status
