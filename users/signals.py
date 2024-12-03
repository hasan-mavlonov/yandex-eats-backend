import threading

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
    PhoneVerification.objects.create(user=User.objects.get(phone=phone),
                                     phone_verification_code=phone_verification_code)
    recipient_list = [phone]
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for recipient in recipient_list:
        print(recipient)
        if recipient:
            client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    return HttpResponse("messages sent!" + message_to_broadcast, 200)


@receiver(post_save, sender=User)
def send_confirmation_code(sender, instance=None, created=False, **kwargs):
    if created:
        phone_thread = threading.Thread(target=send_verification_phone, args=(instance.phone,))
        phone_thread.start()
