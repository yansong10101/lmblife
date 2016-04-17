from core.models import Customer, University, OrgAdmin, CustomerUPG, FeatureGroup, Feature, Permission, PermissionGroup
from core.serializers import (UniversityListSerializer, UniversityRetrieveSerializer,
                              OrgAdminListSerializer, OrgAdminRetrieveSerializer, CustomerListSerializer,
                              CustomerRetrieveSerializer, PermissionListSerializer, PermissionRetrieveSerializer,
                              PermissionGroupListSerializer, PermissionGroupRetrieveSerializer,
                              CustomerUPGListSerializer, CustomerUPGRetrieveSerializer, FeatureGroupListSerializer,
                              FeatureGroupRetrieveSerializer, FeatureListSerializer, FeatureRetrieveSerializer,
                              FeatureSlugSerializer)
from core.forms import (UniversityForm, OrgAdminCreateForm, CustomerCreationForm, CustomerUPGForm, FeatureGroupForm,
                        FeatureForm, PermissionGroupForm)
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from lmb_api.utils import (response_message, to_json, generate_key, set_email_verification_cache)
from message.emailer import Email, TYPE_SIGNUP
# from django.contrib.sites.models import Site


# University APIs
class UniversityList(generics.ListAPIView):
    queryset = University.universities
    serializer_class = UniversityListSerializer
    paginate_by = 15


class UniversityRetrieve(generics.RetrieveAPIView):
    queryset = University.universities
    serializer_class = UniversityRetrieveSerializer


@api_view(['POST', 'PUT', ])
def create_update_university(request, pk=None):
    # TODO : If create university
    """
        create new university:
        1. create a super user (president)
        2. grant all permissions to president
        3. can create group ?
        4. create S3 initial keys -- v
    """

    def init_org_s3_keys(uni_org):
        from content import make_org_s3_initial_directory_names, S3, AWS_BUCKET_ORG_WIKI, WIKI_TEMPLATE_ROOT
        initial_dict = make_org_s3_initial_directory_names(uni_org.slug_name, uni_org.pk)

        s3_con = S3(AWS_BUCKET_ORG_WIKI)
        init_file = '/'.join((WIKI_TEMPLATE_ROOT, '_init.json'))
        for key_path in initial_dict.values():
            s3_con.upload_wiki(init_file, key_path)

    response_data = {}
    if request.method == 'POST' or request.method == 'PUT':
        if pk is None:
            form = UniversityForm(request.POST)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            org = University.create(**form.cleaned_data)
            init_org_s3_keys(org)
        else:
            university = get_object_or_404(University, pk=pk)
            form = UniversityForm(request.POST, instance=university)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            form.save()
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    return Response(data=response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Org Admin APIs
class OrgAdminList(generics.ListAPIView):
    queryset = OrgAdmin.org_admins
    serializer_class = OrgAdminListSerializer
    paginate_by = 15


class OrgAdminRetrieve(generics.RetrieveAPIView):
    queryset = OrgAdmin.org_admins
    serializer_class = OrgAdminRetrieveSerializer


@api_view(['POST', ])
def create_org_admin(request):
    response_data = {}
    if request.method == 'POST':
        form = OrgAdminCreateForm(request.POST)
        if not form.is_valid():
            return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
        form.clean_password2()
        form.save()
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    return Response(data=response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Customer APIs
class CustomerList(generics.ListAPIView):
    queryset = Customer.customers
    serializer_class = CustomerListSerializer
    paginate_by = 15


class CustomerRetrieve(generics.RetrieveAPIView):
    queryset = Customer.customers
    serializer_class = CustomerRetrieveSerializer


@api_view(['POST', ])
def create_customer(request):
    response_data = {}
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        domain_name = request.META['HTTP_HOST']
        if not form.is_valid():
            return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
        form.clean_password2()
        user = form.save()
        # generate token and cache user data
        token = generate_key(long_token=True)
        set_email_verification_cache(token, user.email)
        # send verification email
        mail = Email([user.email, ], TYPE_SIGNUP)
        mail.send_mail_welcome({'username': user.email,
                                'url': '"{}/{}/?token={}"'.format(domain_name, 'api/portal/email-token-verification', token)})
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    return Response(data=response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# CustomerUPG APIs
class CustomerUPGList(generics.ListAPIView):
    queryset = CustomerUPG.customer_upg
    serializer_class = CustomerUPGListSerializer
    paginate_by = 15


class CustomerUPGRetrieve(generics.RetrieveAPIView):
    queryset = CustomerUPG.customer_upg
    serializer_class = CustomerUPGRetrieveSerializer


@api_view(['POST', ])
def create_customer_upg(request):
    response_data = dict()
    if request.method == 'POST':
        form = CustomerUPGForm(request.POST)
        if not form.is_valid():
            return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data['result'] = form.create_customer_upg()
        return Response(data=to_json(response_data), status=status.HTTP_200_OK)
    return Response(data=response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
def update_customer_upg(request):
    response_data = dict()
    if request.method == 'POST':
        form = CustomerUPGForm(request.POST)
        if not form.is_valid():
            return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data['result'] = form.update_customer_upg()
        return Response(data=to_json(response_data), status=status.HTTP_200_OK)
    return Response(data=response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', ])
def get_customer_upg_by_university(request):
    if request.method == 'GET':
        response_data = list()
        university = request.GET['university'] or None
        if not university:
            return Response(data=response_message(message='Invalid parameter'), status=status.HTTP_400_BAD_REQUEST)
        university_upg = CustomerUPG.customer_upg.get_org_deserved_customer_upg(university)
        for upg in university_upg:
            response_data.append(model_to_dict(upg))
        return Response(data={'result': response_data}, status=status.HTTP_200_OK)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Feature Group APIs
class FeatureGroupList(generics.ListAPIView):
    queryset = FeatureGroup.feature_groups
    serializer_class = FeatureGroupListSerializer
    paginate_by = 15


class FeatureGroupDetail(generics.RetrieveAPIView):
    queryset = FeatureGroup.feature_groups
    serializer_class = FeatureGroupRetrieveSerializer


@api_view(['POST', 'PUT', ])
def create_update_feature_group(request, pk=None):
    """
        We do not check permission since the feature group is only created by LMB internally,
        all universities should have the same visibility of all base feature groups.
    """
    if request.method == 'POST' or request.method == 'PUT':
        if pk is None:
            form = FeatureGroupForm(request.POST)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            FeatureGroup.create(**form.cleaned_data)
        elif pk:
            feature_group = get_object_or_404(FeatureGroup, pk=pk)
            form = FeatureGroupForm(request.POST, instance=feature_group)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            form.save()
        return Response(data=response_message(code=201), status=status.HTTP_201_CREATED)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Feature APIs
class FeatureList(generics.ListAPIView):
    queryset = Feature.features
    serializer_class = FeatureListSerializer
    paginate_by = 15


class FeatureDetail(generics.RetrieveAPIView):
    queryset = Feature.features
    serializer_class = FeatureRetrieveSerializer


class FeatureSlugView(generics.RetrieveAPIView):
    queryset = Feature.features
    serializer_class = FeatureSlugSerializer


@api_view(['POST', 'PUT', ])
def create_update_feature(request, pk=None):
    if request.method == 'POST' or request.method == 'PUT':
        if pk is None:
            form = FeatureForm(request.POST)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            Feature.create_feature(**form.cleaned_data)
        elif pk:
            feature = get_object_or_404(Feature, pk=pk)
            form = FeatureForm(request.POST, instance=feature)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            form.save()
        return Response(data=response_message(code=201), status=status.HTTP_201_CREATED)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Permission APIs
class PermissionList(generics.ListAPIView):
    queryset = Permission.permissions
    serializer_class = PermissionListSerializer
    paginate_by = 15


class PermissionRetrieve(generics.RetrieveAPIView):
    queryset = Permission.permissions
    serializer_class = PermissionRetrieveSerializer


def create_permission():
    """
        We do not allow to create permission via API, until only new feature creation triggered.
    """
    pass


# Permission Group APIs
class PermissionGroupList(generics.ListAPIView):
    queryset = PermissionGroup.permission_groups
    serializer_class = PermissionGroupListSerializer
    paginate_by = 15


class PermissionGroupRetrieve(generics.RetrieveAPIView):
    queryset = PermissionGroup.permission_groups
    serializer_class = PermissionGroupRetrieveSerializer


@api_view(['POST', 'PUT', 'DELETE', ])
def create_update_permission_group(request, pk=None):
    """
    :param request: required fields: list of permission IDs-> permissions, string -> permission_name
    :return: response with HTTP status code
    """
    if request.method == 'POST' or request.method == 'PUT':
        response_data = {}
        permission_list = [int(i) for i in request.POST.getlist('permissions[]')]
        if pk is None:
            form = PermissionGroupForm(request.POST)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            PermissionGroup.create(permission_list, **form.cleaned_data)
        elif pk:
            permission_group = get_object_or_404(PermissionGroup, pk=pk)
            form = PermissionGroupForm(request.POST, instance=permission_group)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            form.save()
            if permission_list:
                PermissionGroup.update(permission_group, permission_list)
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE' and pk:
        # NOTE : de-active only for now, better to delete with all relations ?
        permission_group = get_object_or_404(PermissionGroup, pk=pk)
        permission_group.is_active = False
        permission_group.save()
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
