from prometheus_client import Gauge, Counter, Summary, Histogram


class Prom:
    SEND_SMS_NOTIFICATION = Summary('send_sms_notification_latency_seconds', 'Time spent processing send sms notification')
