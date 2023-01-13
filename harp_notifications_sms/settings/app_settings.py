import os

# Flask settings
URL_PREFIX = os.getenv('URL_PREFIX', '/harp-notifications-sms/api/v1')
SERVICE_NAMESPACE = os.getenv('SERVICE_NAMESPACE', 'dev')
POD_NAME = os.getenv('POD_NAME', '')

# Logging
SERVICE_NAME = os.getenv('SERVICE_NAME', 'harp-notifications-sms')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOKI_SERVER = os.getenv('LOKI_SERVER', '')
LOKI_PORT = os.getenv('LOKI_PORT', 3100)

BOTS_SERVICE = os.getenv('BOTS_SERVICE', '')


class TracingConfig:
    TEMPO_URL = os.getenv('TEMPO_URL', '')
