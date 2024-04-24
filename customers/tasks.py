from celery import shared_task
from icecream import ic
from datetime import date
from django.core.mail import EmailMessage
from customers.models import Customer
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_birthday_email_greetings():
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
                logger.warning('Sender email not configured, printing the email body in the console instead')
                logger.info(f'Email subject: {email.subject}')
                logger.info(f'Email body: {email.body}')

    except Exception as e:
        ic(e)
