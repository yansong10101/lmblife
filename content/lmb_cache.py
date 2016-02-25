from django.core.cache import cache, caches
from datetime import datetime

"""
We use MEMCACHE now for storing frequent data querying,
"""


_TOKEN_EXPIRED = 60 * 60 * 24  # hard code for 1 day
_USER_CACHE_EXPIRED = 60 * 60 * 24  # hard code for 1 day
_LONG_TERM_CACHE_EXPIRED = 0  # 30 days or never


class LMBCache:

    def __set__(self, key, value, timeout, version=None):
        try:
            cache.set(key, value, timeout=timeout, version=version)
        except ConnectionError:
            raise Exception('Invalid cache set !')
        return True

    def __get__(self, key):
        try:
            result = cache.get(key)
        except LookupError:
            raise Exception('Key: %s Not found !' % key)
        return result

    def set_token(self, token, value, version=None):
        return self.__set__(token, value, _TOKEN_EXPIRED, version)

    def set_user(self, user_identifier, value, version=None):
        return self.__set__(user_identifier, value, _USER_CACHE_EXPIRED, version)

    def set_long_term(self, key, value, version=None):
        return self.__set__(key, value, _LONG_TERM_CACHE_EXPIRED, version)

    def get(self, key):
        return self.__get__(key)

    def is_exists(self, key):
        if self.__get__(key):
            return True
        return False

    def __delete__(self, key, version=None):
        try:
            cache.delete(key, version=version)
        except LookupError:
            raise Exception('Key: %s Not found !' % key)
        return True

    def delete(self, key, version=None):
        return self.__delete__(key, version)

    @classmethod
    def make_datetime_version(cls):
        return datetime.now().strftime('%Y-%m-%d %H:%M')

    @classmethod
    def all(cls):
        return caches.all()
