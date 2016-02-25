import os
import smtplib
from mailer import send_mail, send_html_mail, models as mail_model
from lmblife.settings import EMAIL_HOST, EMAIL_PORT
from message.mail_settings import EMAIL_TEMPLATE_ROOT, EMAIL_ACCOUNT_MAP
from string import Template
from lmb_api.utils import LMBEmailTemplateFailed


EMAIL_BACKEND = "mailer.backend.DbBackend"
MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# email type mapping takes shortcut of basic email info setup
# value list contains: [email_type, subject, template, priority]
# TODO : django-mailer cannot setup multiple mail server, it will read default when flush queue
_email_spec_mapping = {
    'default': ('noreply', '[notification] notification do not reply', '', mail_model.PRIORITY_MEDIUM),
    'signup': ('noreply', '[Welcome] Welcome to join 留美帮', 'signup.html', mail_model.PRIORITY_HIGH),
    'reset_password': ('noreply', '[Important] Your request to reset password', '', mail_model.PRIORITY_HIGH),
    'log_exceptions': ('support', '[Exception] Site Exception', '', mail_model.PRIORITY_HIGH),
}


class Email:

    """
        Initial mail template and send to single or multiple users by email.
        email generator will check email type and use the right template.
    """

    def __init__(self, recipient_list, email_for, subject=None, priority=None, fail_silently=False):

        if email_for not in _email_spec_mapping.keys():
            email_for = 'default'
        email_specs = _email_spec_mapping[email_for]
        (self.auth_user, self.auth_password) = EMAIL_ACCOUNT_MAP[email_specs[0]]
        self.subject = subject or email_specs[1]
        self.recipient_list = recipient_list
        self.priority = priority or email_specs[3]
        self.fail_silently = fail_silently

        self.mail_server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        self.mail_server.ehlo()
        self.mail_server.starttls()
        self.mail_server.ehlo()
        self.mail_server.login(self.auth_user, self.auth_password)

    def _send_mail(self, body, body_html=None, header=None):

        if body_html:
            mail_header = header or dict()
            send_html_mail(self.subject,
                           body,
                           body_html,
                           self.auth_user,
                           self.recipient_list,
                           self.priority,
                           self.fail_silently,
                           self.auth_user,
                           self.auth_password,
                           mail_header)
        else:
            send_mail(self.subject,
                      body,
                      self.auth_user,
                      self.recipient_list,
                      self.priority,
                      self.fail_silently,
                      self.auth_user,
                      self.auth_password)

    def send_mail_welcome(self, substitute_dict):
        body_html = Email.make_template('signup', substitute_dict)
        self._send_mail('', body_html)

    @classmethod
    def make_template(cls, email_for, substitute_dict):
        file_name = _email_spec_mapping[email_for][2]
        template_file = '/'.join((EMAIL_TEMPLATE_ROOT, file_name))
        if not os.path.isfile(template_file):
            raise Exception(' '.join(('No template found or not a file: ', template_file)))
        try:
            template = Template(open(template_file).read())
            result = template.substitute(substitute_dict)
            return result
        except LMBEmailTemplateFailed:
            raise Exception(' '.join(('failed generate email: ', email_for)))
