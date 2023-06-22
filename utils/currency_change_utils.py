from utils import currency_utils
from utils.network_utils import get_ip, client_country
from accounts.models import AuthUsers, CurrencyChoices


def exchange(currency: str, price: float) -> float:
    usd_exchange_rate = float(currency_utils.get_currencies()['USD'])

    if currency == CurrencyChoices.CURRENCY_UZS:
        price = price * usd_exchange_rate

    elif currency == CurrencyChoices.CURRENCY_USD:
        pass

    else:
        code = {
            '₽': 'RUB',
            '¥': 'CNY'
        }[currency]

        exchange_rate = float(currency_utils.get_currencies()[code])
        price = (price * usd_exchange_rate) / exchange_rate

    price = float("{:.2f}".format(price))
    return price


def user_currency(request, price: float) -> (str, float):
    if price:
        if request.user.is_authenticated:
            current_user = AuthUsers.objects.get(email__exact=request.user.email)
            currency = CurrencyChoices.CURRENCY_USD

            if current_user.currency == 'UZS':
                currency = CurrencyChoices.CURRENCY_UZS

            elif current_user.currency == '¥':
                currency = CurrencyChoices.CURRENCY_CNY

            elif current_user.currency == '₽':
                currency = CurrencyChoices.CURRENCY_RUB

            price = exchange(currency, price)
            return currency, price

        else:
            ip = get_ip(request)
            country_code, country_name = client_country(ip)
            currency = CurrencyChoices.CURRENCY_USD

            if country_code == 'UZ':
                currency = CurrencyChoices.CURRENCY_UZS

            elif country_code == 'CN':
                currency = CurrencyChoices.CURRENCY_CNY

            elif country_code == 'RU':
                currency = CurrencyChoices.CURRENCY_RUB

            price = exchange(currency, price)
            return currency, price

    else:
        currency = CurrencyChoices.CURRENCY_UZS
        price = None
        return currency, price







