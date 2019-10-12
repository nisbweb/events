import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
sentry_sdk.init(
    dsn="https://65b184a9707d4fec9602a1dde3454981@sentry.io/1777578",
    integrations=[FlaskIntegration()]
)