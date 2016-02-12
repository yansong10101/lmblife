from lmb import *
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from lmb_api.utils import response_message


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
    """
    response_data = {}
    if request.method == 'POST' or request.method == 'PUT':
        if pk is None:
            form = UniversityForm(request.POST)
            if not form.is_valid():
                return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
            University.create(**form.cleaned_data)
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
        if not form.is_valid():
            return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
        form.clean_password2()
        form.save()
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
def create_update_customer_upg(request):
    response_data = {}
    if request.method == 'POST':
        form = CustomerUPGForm(request.POST)
        if not form.is_valid():
            return Response(data=form.errors.as_data(), status=status.HTTP_400_BAD_REQUEST)
        if not form.validate_existing():
            CustomerUPG.create_customer_upg(**form.cleaned_data)
        else:
            form.update_customer_university_group()
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    return Response(data=response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
        We do not check permission since the feature group is only created by LMB internal team,
        all university should have the same visibility of all base feature groups.
    """
    response_data = {}
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
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Feature APIs
class FeatureList(generics.ListAPIView):
    queryset = Feature.features
    serializer_class = FeatureListSerializer
    paginate_by = 15


class FeatureDetail(generics.RetrieveAPIView):
    queryset = Feature.features
    serializer_class = FeatureRetrieveSerializer


@api_view(['POST', 'PUT', ])
def create_update_feature(request, pk=None):
    if request.method == 'POST' or request.method == 'PUT':
        response_data = {}
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
        return Response(data=response_data, status=status.HTTP_201_CREATED)
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
            PermissionGroup.permission_groups.create_permission_group(permission_list, **form.cleaned_data)
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
