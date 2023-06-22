import json

from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
from django.utils.translation import get_language


def get_ip(request) -> str:
    """
    Function for getting an IP of the user
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def translate_country(country_code: str, country_name: str) -> tuple[str, str]:
    """
    Function gets user's country code and
    returns translation based on the settings of a user in the web-site
    """
    try:
        file_dir = f"{settings.BASE_DIR}/locale/countries/{get_language()}.json"
        print(file_dir)
        with open(file_dir) as file:
            data = json.load(file)
            country_name = data[country_code]['name']
    except:
        pass
    return country_code, country_name


def client_country(ip: str) -> tuple[str, str]:
    """
    Function gets user IP and returns his located country
    with the translation to language user set in the web-site
    """
    g = GeoIP2()
    try:
        result = g.country(ip)
        country_code, country_name = translate_country(
            country_code=result['country_code'],
            country_name=result['country_name']
        )
    except AddressNotFoundError or KeyError:
        country_code = 'UZ'
        country_name = 'NOT DETERMINED'
    return country_code, country_name
