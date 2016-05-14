from django.contrib.auth import logout as django_logout, login as django_login
from core.forms import (UserAuthenticationForm, UserChangePasswordForm, UserResetPassword, GrantUserPermissionForm,
                        UserForgotPassword, UserAvatarFileForm)
from lmb_api.utils import (response_message, refresh_or_create_user_cache, Cache, update_admin_permission_group,
                           check_request_user_role, email_verification, reset_password_cache_handler)
from lmb_api.restful.core_api import (create_customer, update_customer_upg, create_customer_upg,
                                      get_customer_upg_by_university)
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from message.emailer import Email, TYPE_RESET_PASSWORD
from lmblife.settings import AWS_BUCKET_USER_ARCHIVE
from content import S3


@api_view(['POST', ])
@parser_classes((JSONParser,))
def login(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.data)
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


@api_view(['POST', ])
def reset_password(request):
    if request.method == 'POST':
        form = UserResetPassword(request.POST)
        if form.is_valid():
            form.reset_password()
            return Response(data=response_message(code=200), status=status.HTTP_200_OK)
        return Response(data=response_message(message='Invalid password'), status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def forgot_password_email(request):
    if request.method == 'POST':
        form = UserForgotPassword(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                token = reset_password_cache_handler(user.email)
                mail = Email([user.email, ], TYPE_RESET_PASSWORD)
                mail.send_mail_welcome({'username': user.email,
                                        'url': '"{}/{}/?code={}"'.format('https://www.lmeib.com', '/user/reset',
                                                                          token)})
            return Response(data=response_message(code=200), status=status.HTTP_200_OK)
        return Response(data=response_message(message='Username Does not exist !'), status=status.HTTP_400_BAD_REQUEST)
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
    return create_customer_upg(request)


@api_view(['POST', ])
def grant_university_permission(request):
    return update_customer_upg(request)


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


@api_view(['POST', ])
def upload_user_avatar(request, ):
    s3 = S3(AWS_BUCKET_USER_ARCHIVE)
    if request.method == 'POST':
        form = UserAvatarFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
        key_prefix = form.make_avatar_s3_key_prefix()
        s3_key = s3.upload_image(request.FILES['file'], key_prefix)
        image_url = form.update_user_avatar_key(AWS_BUCKET_USER_ARCHIVE, s3_key)
        return Response(data={'image_url': image_url}, status=status.HTTP_201_CREATED)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
