from django.contrib.auth import logout as django_logout, login as django_login
from core.forms import (UserAuthenticationForm, UserChangePasswordForm, UserResetPassword, GrantUserPermissionForm)
from lmb_api.utils import (response_message, refresh_or_create_user_cache, is_authenticate_user, get_cache, Cache,
                           update_admin_permission_group, check_request_user_role, email_verification)
from lmb_api.restful.core_api import create_customer, create_update_customer_upg, get_customer_upg_by_university
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST', ])
def login(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            (user, token) = form.authenticate()
            if user:
                django_login(request, user)
                response_data = dict({'result': 'success', 'data': refresh_or_create_user_cache(token, user), })
                return Response(data=response_data, status=status.HTTP_200_OK)
        return Response(data=response_message(message='Invalid username or password'),
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def customer_signup(request):
    return create_customer(request)


@api_view(['POST', ])
def logout(request):
    if request.method == 'POST':
        token = request.POST['token']
        user_cache = Cache()
        user_cache.delete(token)
        django_logout(request)
        return Response(data={}, status=status.HTTP_200_OK)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def change_password(request):
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            user = form.set_password()
            if user:
                django_login(request, user)
                return Response(data=response_message(code=200), status=status.HTTP_200_OK)
        return Response(data=response_message(message='Invalid password'), status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', 'GET', ])
def reset_password(request):
    if request.method == 'GET':
        token = request.POST['token']
        if is_authenticate_user(token):
            return Response(data=get_cache(token), status=status.HTTP_302_FOUND)
        return Response(data=response_message(message='expired link'), status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        form = UserResetPassword(request.POST)
        if form.is_valid():
            user = form.reset_password()
            if user:
                django_login(request, user)
                return Response(data=response_message(code=200), status=status.HTTP_200_OK)
        return Response(data=response_message(message='Invalid password'), status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def grant_admin_permission_groups(request):
    if request.method == 'POST':
        form = GrantUserPermissionForm(request.POST)
        permission_group_list = [int(i) for i in request.POST.getlist('permission_groups[]')]
        if form.is_valid() and permission_group_list and check_request_user_role(request.POST['token'], ('president',)):
            user = form.authenticate()
            update_admin_permission_group(user, permission_group_list)
            return Response(data=response_message(code=200), status=status.HTTP_200_OK)
        return Response(data=response_message(message='Invalid inputs'), status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def apply_university_permission(request):
    return create_update_customer_upg(request)


@api_view(['GET', ])
def management_list_upg(request):
    return get_customer_upg_by_university(request)


@api_view(['GET', ])
def refresh_user_cache(request):
    if request.method == 'GET':
        token = request.GET['token']
        response_data = dict({'result': 'success', 'data': refresh_or_create_user_cache(token), })
        return Response(data=response_data, status=status.HTTP_200_OK)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', ])
def email_token_verification(request):
    if request.method == 'GET':
        token = request.GET['token'] or None
        return Response(data={'is_verified': email_verification(token), }, status=status.HTTP_200_OK)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
