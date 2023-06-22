from utils.models_utils import get_valid_craftmanship, get_valid_sections
from utils.network_utils import get_ip, client_country
from general.models import Sections, About, Services
from utils.cart_utils import get_cart_items_count
from utils.currency_utils import get_currencies


def get_common_context(request, work=None):
    user = request.user
    currencies = get_currencies()
    ip = get_ip(request=request)
    sections = get_valid_sections()
    cart_items = get_cart_items_count(user)
    craftmanship = get_valid_craftmanship()
    abouty = About.objects.all().order_by("order")
    servicesy = Services.objects.all().order_by("order")
    country_code, country_name = client_country(ip)

    common_context = {
        "country_name": country_name,
        "currencies": currencies,
        "craftmanship": craftmanship,
        "sections": sections,
        "cart_items": cart_items,
        "abouty": abouty,
        "servicesy": servicesy,
    }

    if work:
        common_context['work'] = work
    return common_context
