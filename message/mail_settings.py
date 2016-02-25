import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_BACKEND = "mailer.backend.DbBackend"
MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_ACCOUNT_MAP = {
    # support email for contacts and communication etc
    'support': (os.environ.get('QA_EMAIL', None), os.environ.get('QA_EMAIL_PASSWORD', None)),
    # non-reply email for sending confirmation email etc
    'noreply': (os.environ.get('QA_EMAIL', None), os.environ.get('QA_EMAIL_PASSWORD', None)),
    # service email for sending credential or receipts etc
    'service': (os.environ.get('QA_EMAIL', None), os.environ.get('QA_EMAIL_PASSWORD', None)),
    # sending for new feature, functionality etc
    'marketing': (os.environ.get('QA_EMAIL', None), os.environ.get('QA_EMAIL_PASSWORD', None)),
}

EMAIL_TEMPLATE_ROOT = os.path.join(BASE_DIR, 'templates/mailer')
