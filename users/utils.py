import random

from users.models import PhoneVerification



def get_random_phone_verification_code(phone):
    phone_verification_code = random.randint(1000, 9999)
    if PhoneVerification.objects.filter(user__phone=phone,
                                             phone_verification_code=phone_verification_code).exists():
        phone_verification_code = random.randint(1000, 9999)
    return phone_verification_code
