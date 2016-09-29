import binascii
import os
from lmb_core.customer.models import Customer
from content.lmb_cache import LMBCache as Cache


def generate_token(long_token=False):
    if long_token:
        return binascii.hexlify(os.urandom(40)).decode()
    return binascii.hexlify(os.urandom(32)).decode()


def parse_auth_token(token):
    if token:
        return token.split()[-1]
    return None


def _refresh_or_reset_cache(token, value):
    # Assume the token will be always unique
    ch = Cache()
    if not ch.is_exists(token):
        token = generate_token()
    ch.set_user(token, value)
    return token


def get_customer_from_cache(auth):
    cached_data = Cache().get(parse_auth_token(auth))
    if not cached_data:
        return None
    return Customer.customers.get_customer_by_email(cached_data['email'])


def set_customer_to_cache(token, customer):
    customer_dict = customer.make_attr_dict(['email', 'first_name', 'last_name', 'last_login_date', ])
    return _refresh_or_reset_cache(parse_auth_token(token), customer_dict)
