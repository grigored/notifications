from typing import Optional

from raven.contrib.flask import Sentry

SENTRY_LIST_MAX_LENGTH = 100
SENTRY_STRING_MAX_LENGTH = 100000

sentry: Optional[Sentry] = None


def capture_sentry_exception() -> None:
    global sentry
    sentry and sentry.captureException()


def capture_sentry_message(message: str) -> None:
    global sentry
    sentry and sentry.captureMessage(message, stack=True)


# TODO: Unused function
def get_sentry() -> Sentry:
    global sentry
    # if sentry is None:
    #     raise Exception
    return sentry


def set_sentry(new_sentry: Sentry) -> None:
    global sentry
    sentry = new_sentry
