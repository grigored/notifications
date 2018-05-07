import requests

from src.configs.sentry_conf import capture_sentry_message, capture_sentry_exception


def send_slack_message(message: str):
    try:
        response = requests.post(
            'https://hooks.slack.com/services/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',
            json={'text': message},
            headers={'Content-Type': 'application/json'},
        )
        if response.status_code != 200:
            response_text = response.text
            response_status = response.status_code
            capture_sentry_message('SLACK_MESSAGE_FAILED')
    except:
        capture_sentry_exception()
