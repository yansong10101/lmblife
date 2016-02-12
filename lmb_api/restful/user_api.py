from django.contrib.auth import logout as django_logout, login as django_login
from lmb_api.utils import (response_message, cache_user, is_authenticate_user, update_admin_permission_group,
                           get_cache, Cache)
from lmb_api.restful.lmb_api import create_customer
from lmb import (UserAuthenticationForm, UserChangePasswordForm, UserResetPassword, GrantUserPermissionForm)
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
                response_data = dict({'result': 'success', 'data': cache_user(user, token), })
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
    # FIXME : Check if user login as president
    if request.method == 'POST':
        form = GrantUserPermissionForm(request.POST)
        permission_group_list = [int(i) for i in request.POST.getlist('permission_groups[]')]
        if form.is_valid() and permission_group_list:
            user = form.authenticate()
            update_admin_permission_group(user, permission_group_list)
            return Response(data=response_message(code=200), status=status.HTTP_200_OK)
        return Response(data=response_message(message='Invalid inputs'), status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
