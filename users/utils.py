import random

from users.models import PhoneVerification

import requests


def get_random_phone_verification_code(phone):
    phone_verification_code = random.randint(1000, 9999)
    if PhoneVerification.objects.filter(user__phone=phone,
                                        phone_verification_code=phone_verification_code).exists():
        phone_verification_code = random.randint(1000, 9999)
    return phone_verification_code


def get_location_from_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    # Fallback if behind proxy or load balancer
    if not ip or ip == '127.0.0.1':
        ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        data = response.json()

        # Extract and format longitude and latitude to 6 decimal places
        longitude = round(data.get('lon', 0), 6)
        latitude = round(data.get('lat', 0), 6)

        return longitude, latitude

    except requests.exceptions.RequestException as e:
        print(f"Error fetching location for IP {ip}: {e}")
        return None, None
