import threading
from random import randint

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from twilio.rest import Client

from users.models import User, PhoneVerification
from users.utils import get_random_phone_verification_code
from conf import settings


def send_verification_phone(phone):
    phone_verification_code = get_random_phone_verification_code(phone=phone)
    message_to_broadcast = f'Your verification code is: {phone_verification_code}'
    user = User.objects.get(phone=phone)
    PhoneVerification.objects.create(user=user, phone_verification_code=phone_verification_code)
    recipient_list = [phone]
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for recipient in recipient_list:
        if recipient:
            client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    return "Messages sent!"


def send_verification_code(phone):
    verification_code = str(randint(100000, 999999))

    # Create PhoneVerification object for the user
    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return

    PhoneVerification.objects.create(user=user, phone_verification_code=verification_code)

    # Send the code via SMS using Twilio
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = f'Your verification code is: {verification_code}'
    client.messages.create(to=phone, from_=settings.TWILIO_NUMBER, body=message)