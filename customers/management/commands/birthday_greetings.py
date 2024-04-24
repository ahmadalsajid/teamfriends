from icecream import ic
from datetime import date
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from customers.models import Customer
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Send birthday greetings to the customers on their birthdays"

    def handle(self, *args, **options):
        try:
            _today = date.today()
            _birthdays_today = Customer.objects.filter(
                date_of_birth__day=_today.day,
                date_of_birth__month=_today.month,
            )
            for _user in _birthdays_today:
                _email_subject = f'Happy birthday {_user.name}'
                _email_body = f'Dear {_user.name}, happy birthday to you.'
                email = EmailMessage(
                    _email_subject, _email_body, None, [f'{_user.email}'])
                try:
                    email.send()
                    logger.info(email.body)
                except Exception as e:
                    ic(e)
                    logger.info('Sender email not configured, printing the email boy in the console instead')
                    logger.info(f'Email subject: {email.subject}')
                    logger.info(f'Email body: {email.body}')

        except Exception as e:
            ic(e)
