import binascii
import os
from content import Cache
from core.models import OrgAdmin, Customer, CustomerUPG
import json
import datetime
from django.db.models.base import ModelState


_LMBBadRequest = u'Malformed request'
_LMBUnauthorizedUser = u'Unauthorized user permission !'
_LMBMethodNotAllowed = u'HTTP METHOD IS NOT ALLOWED'


def generate_key(long_token=False):
        if long_token:
            return binascii.hexlify(os.urandom(40)).decode()
        return binascii.hexlify(os.urandom(20)).decode()


def to_json(obj):
    def _handler(o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, ModelState):
            return None
        else:
            return {key: value for key, value in o.__dict__.items() if not key.startswith('_')}
    return json.dumps(obj, default=lambda o: _handler(o))


def get_cache(key):
    lmb_cache = Cache()
    return lmb_cache.get(key)


def get_cached_user(token):
    return get_cache(token)


def get_cached_user_by_email(token):
    cached_data = get_cache(token)
    if not cached_data:
        return None
    email = cached_data['email'] or None
    return Customer.customers.get_auth_customer(email) or None


def get_cached_user_by_token(token):
    cached_data = get_cache(token)
    if check_request_user_role(cached_data, ('customer', )):
        return Customer.customers.get_auth_customer(cached_data['username']) or None


def _get_user_by_username(username):
    return Customer.customers.get_auth_customer(username) or OrgAdmin.org_admins.get_auth_admin(username)


def _cache_user(user):
    response_data = dict()
    if isinstance(user, Customer):
        response_data['user_id'] = user.pk
        response_data['email'] = response_data['username'] = user.email
        response_data['avatar'] = user.avatar_url
        response_data['first_name'] = user.first_name
        response_data['last_name'] = user.last_name
        response_data['role'] = 'customer'
        response_data['is_approved'] = user.is_approved
        response_data['email_check'] = user.is_email_verified
        response_data['permission_groups'] = list()
        upg_list = CustomerUPG.customer_upg.all().filter(customer=user)
        for upg in upg_list:
            # TODO : Required default permission ? Feature ? When apply ?
            org_feature_permissions = list()
            if upg.permission_group:
                org_feature_permissions = [dict(permision_id=permission.pk,
                                                permission_type=permission.permission_type,
                                                feature_id=permission.feature.pk or None,
                                                feature_name=permission.feature.feature_name or None)
                                           for permission in upg.permission_group.permission.all()]
            response_data['permission_groups'].append(dict({'university_id': upg.university.pk,
                                                            'university_handle': upg.university.handle,
                                                            'university_slug': upg.university.slug_name,
                                                            'handle': upg.university.handle,
                                                            'feature_permissions': org_feature_permissions,
                                                            'grant_level': upg.grant_level, }))
    elif isinstance(user, OrgAdmin):
        response_data['user_id'] = user.pk
        response_data['username'] = user.username
        response_data['role'] = 'admin'
        response_data['university_id'] = user.university.pk
        response_data['university_handle'] = user.university.handle
        response_data['university_slug'] = user.university.slug_name
        response_data['handle'] = user.university.handle
        response_data['permission_groups'] = list()
        if user.is_president:
            response_data['role'] = 'president'
        for group in user.permission_group.all():
            org_feature_permissions = [dict(permision_id=permission.pk,
                                            permission_type=permission.permission_type,
                                            feature_id=permission.feature.pk or None,
                                            feature_name=permission.feature.feature_name or None)
                                       for permission in group.permission.all()]
            response_data['permission_groups'].append(dict(permission_group_name=group.group_name,
                                                           permission_group_id=group.pk,
                                                           feature_permissions=org_feature_permissions))
    else:
        raise Exception(LMBError(content=user))
    return response_data


def refresh_or_create_user_cache(token, user=None):
    cache = Cache()
    if cache.is_exists(token):
        user_cache = cache.get(token)
        user = _get_user_by_username(user_cache['username'])
    else:
        if not user:
            raise Exception('Bad request !')
        # generate a new unique token
        token = generate_key()
        while cache.is_exists(token):
            token = generate_key()
    user_data = _cache_user(user)
    user_data['token'] = token
    user_data['last_modified'] = cache.make_datetime_version()
    cache.set_user(token, user_data)
    return user_data


def set_email_verification_cache(token, cache_dict):
    cache = Cache()
    if token:
        cache.set_token(token, cache_dict)


def is_authenticate_user(token):
    lmb_cache = Cache()
    if lmb_cache.is_exists(token):
        return True
    return False


def email_verification(token):
    if is_authenticate_user(token):
        data = get_cache(token)
        customer = Customer.customers.get_auth_customer(data['email']) or None
        if customer:
            customer.is_email_verified = True
            customer.save()
            return True
    return False


def reset_password_cache_handler(email):
    token = generate_key(long_token=True)
    set_email_verification_cache(token, {'email': email, 'action': 'reset_password'})
    return token


def check_request_user_role(source, expect):
    """
    :param source: dict of user cache or token string
    :param expect: list of expects
    :return:
    """
    user = source if isinstance(source, dict) else get_cache(source)
    if user and user['role'] in expect:
        return True
    return False


def update_admin_permission_group(user, permission_groups):
    if isinstance(user, OrgAdmin):
        origin_group = user.permission_group.all()
        for group in origin_group:
            user.permission_group.remove(group)
        for group in permission_groups:
            user.permission_group.add(group)
        user.save()
        return user
    return 'ERROR: No rights to edit !'


def _response_message_handler(code=None, message=None):

    if code:
        status_code_map = {
            200: _response_message_handler(message='success'),
            201: _response_message_handler(message='created'),
            400: _LMBBadRequest,
            401: _LMBUnauthorizedUser,
            405: _LMBMethodNotAllowed,
        }

        print(type(status_code_map), type(status_code_map[code]), str(LMBUnauthorizedUser))

        return {'result': to_json(status_code_map[code])}
    elif message:
        return {'result': message}

    return {'result': LMBError}


def response_message(code=None, message=None):
    return _response_message_handler(code, message)


class LMBError(Exception):
    """
        The Base Exception class which is extended by derived classes
    """

    message = u'Unknown error occurred'

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.__str__()


class LMBBadRequest(LMBError):

    message = u'Malformed request'


class LMBMethodNotAllowed(LMBError):

    message = u'HTTP METHOD IS NOT ALLOWED'


class LMBUnauthorizedUser(LMBError):

    message = u'Unauthorized user permission !'


class LMBEmailTemplateFailed(LMBError):

    message = u'Failed to generate email template !'
