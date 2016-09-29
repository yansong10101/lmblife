from django.utils.functional import SimpleLazyObject
from lmb_core.customer.utils import get_customer_from_cache


def get_user(request):
    return get_customer_from_cache(request.META.get('HTTP_AUTHENTICATION'))


class TokenAuthenticationMiddleware(object):

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django token authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'lmb_core.customer.middleware.TokenAuthenticationMiddleware'."
        )
        customer = SimpleLazyObject(lambda: get_user(request))
        request.COOKIES['customer'] = customer
