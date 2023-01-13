from logger.logging import service_logger
import traceback
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import harp_notifications_sms.settings as settings
from harp_notifications_sms.logic.sms_processor import SMSNotifications
from typing import Optional

log = service_logger()

router = APIRouter(prefix=settings.URL_PREFIX)


class SMSNotification(BaseModel):
    to_number: str
    body: str
    twilio_account_sid: Optional[str]
    twilio_auth_token: Optional[str]
    twilio_phone_number: Optional[str]


@router.post('/notifications/sms')
async def create_notification(row_data: SMSNotification):
    """
    Create new notification
    """

    data = row_data.dict()

    try:
        notification = SMSNotifications(
            twilio_account_sid=data['twilio_account_sid'] if 'twilio_account_sid' in data else None,
            twilio_auth_token=data['twilio_auth_token'] if 'twilio_auth_token' in data else None,
            twilio_phone_number=data['twilio_phone_number'] if 'twilio_phone_number' in data else None
        )
        status = notification.create_notification(
            to_number=data['to_number'],
            body=data['body']
        )

        log.info(
            msg=f"SMS notification has been sent to {data['to_number']}",
            extra={'tags': {}}
        )

        return status

    except Exception as err:
        log.error(
            msg=f"Can`t send SMS notification \nException: {str(err)} \nTraceback: {traceback.format_exc()}",
            extra={'tags': {}})

        raise HTTPException(status_code=500, detail=f"Backend error: {err}")


@router.get('/notifications/sms/{sid}')
async def create_notification(sid: str):
    """
    Get notification info
    """

    try:
        notification = SMSNotifications(
            twilio_account_sid=None,
            twilio_auth_token=None,
            twilio_phone_number=None
        )
        status = notification.check_status(sid=sid)

        return status, 200

    except Exception as err:
        log.error(
            msg=f"Can`t send SMS notification \nException: {str(err)} \nTraceback: {traceback.format_exc()}",
            extra={'tags': {}})

        raise HTTPException(status_code=500, detail=f"Backend error: {err}")
