import re
from decimal import Decimal
from django import template
from django.utils.formats import number_format

register = template.Library()

@register.filter(is_safe=True)
def intcomma(value, use_l10n=True):
    """
    Convert an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    if use_l10n:
        try:
            if not isinstance(value, (float, Decimal)):
                value = int(value)
        except (TypeError, ValueError):
            return intcomma(value, False)
        else:
            return number_format(value, use_l10n=True, force_grouping=True)
    orig = str(value)
    new = re.sub(r"^(-?\d+)(\d{3})", r"\g<1>,\g<2>", orig)
    if orig == new:
        return new
    else:
        return intcomma(new, use_l10n)

@register.filter
def intspace(value):
    import re

    orig = str(value)

    new = re.sub(r"^(-?\d+)(\d{3})", r"\g<1> \g<2>", orig)
    if orig == new:
        return new
    else:
        return intspace(new)