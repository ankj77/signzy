from django.conf import settings

from apps.hotels.helpers import CityHotelHelper


def extra_context(request):
    extra_context = {}
    cities = CityHotelHelper.getCityHotels()

    extra_context = {
        'STATIC_FILE_VERSION': settings.STATIC_FILE_VERSION,
        'PAY_NOW': settings.PAY_NOW,
        'PAY_AT_HOTEL': settings.PAY_AT_HOTEL,
        'CONFIRMATION_MAIL': settings.CONFIRMATION_MAIL,
        'CONFIRMATION_MAIL': settings.OTP,
        'SERVER_EMAIL': settings.SERVER_EMAIL,
        'MINIFY_CSS': settings.MINIFY_CSS,
        'MINIFY_JS': settings.MINIFY_JS,
        'MODIFY_AMOUNT': settings.MODIFY_AMOUNT,
        'treebo_contact': settings.TREEBO_HELPLINE,
        'helpline_contact_caller': settings.HELPLINE_CALLER
    }

    extra_context['cities'] = cities

    return extra_context
