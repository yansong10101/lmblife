import binascii
import os
# from lmb_api.restful.lmb_api import *
from content import Cache
from core.models import OrgAdmin, Customer, CustomerUPG


def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()


def _get_user_permissions(user):
    response_data = dict()
    if isinstance(user, Customer):
        response_data['user_id'] = user.pk
        response_data['email'] = user.email
        response_data['role'] = 'customer'
        response_data['permission_groups'] = list()
        upg_list = CustomerUPG.customer_upg.all().filter(customer=user)
        for upg in upg_list:
            org_feature_permissions = [dict(permision_id=permission.pk,
                                            permission_type=permission.permission_type,
                                            feature_id=permission.feature.pk,
                                            feature_name=permission.feature.feature_name)
                                       for permission in upg.permission_group.permission.all()]
            response_data['permission_groups'].append(dict({'university_id': upg.university.pk,
                                                            'university_name': upg.university.university_name,
                                                            'permission_group_id': upg.permission_group.pk,
                                                            'feature_permissions': org_feature_permissions,
                                                            'grant_level': upg.grant_level, }))
    elif isinstance(user, OrgAdmin):
        response_data['user_id'] = user.pk
        response_data['username'] = user.username
        response_data['role'] = 'admin'
        response_data['university_id'] = user.university.pk
        response_data['university_name'] = user.university.university_name
        response_data['permission_groups'] = list()
        for group in user.permission_group.all():
            org_feature_permissions = [dict(permision_id=permission.pk,
                                            permission_type=permission.permission_type,
                                            feature_id=permission.feature.pk,
                                            feature_name=permission.feature.feature_name)
                                       for permission in group.permission.all()]
            response_data['permission_groups'].append(dict(permission_group_name=group.group_name,
                                                           permission_group_id=group.pk,
                                                           feature_permissions=org_feature_permissions))
    else:
        raise Exception(LMBError(content=user))
    return response_data


def get_or_create_cache_token(token, user_dict):
    user_cache = Cache()
    if user_cache.is_exists(token):
        cached_data = user_cache.get(token)
        if cached_data['user_id'] == user_dict['user_id'] and cached_data['role'] == user_dict['role']:
            user_cache.delete(token)
    token = generate_key()
    while user_cache.is_exists(token):
        token = generate_key()
    user_dict['last_modified'] = user_cache.make_datetime_version()
    user_cache.set_token(token, user_dict)
    return token


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


def cache_user(user, token):
    response_data = _get_user_permissions(user)
    response_data['token'] = get_or_create_cache_token(token, response_data)
    return response_data


def get_cache(key):
    lmb_cache = Cache()
    return lmb_cache.get(key)


def is_authenticate_user(token):
    lmb_cache = Cache()
    if lmb_cache.is_exists(token):
        return True
    return False


def _response_message_handler(code=None, message=None):

    if code:
        status_code_map = {
            200: _response_message_handler(message='success'),
            201: _response_message_handler(message='created'),
            400: LMBBadRequest,
            405: LMBMethodNotAllowed,
        }

        return status_code_map[code]
    elif message:
        return {'result': message}

    return {'result': LMBError}


def response_message(code=None, message=None):
    return _response_message_handler(code, message)


class LMBError:

    message = u'Unknown error occurred. Response content: {content}'

    def __init__(self, url='', status_code='', content='None'):
        self.url = url
        self.status_code = status_code
        self.content = content

    def __str__(self):
        return self.message.format(content=self.content)

    def __unicode__(self):
        return self.__str__()


class LMBBadRequest(LMBError):

    message = u'Malformed request. Response content: {content}'


class LMBMethodNotAllowed(LMBError):

    def __str__(self):
        return u'HTTP METHOD IS NOT ALLOWED'
