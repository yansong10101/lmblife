print('******************************')
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from core.models import University, FeatureGroup, Feature, Permission, PermissionGroup, OrgAdmin, Customer, CustomerUPG

from core.serializers import (UniversityListSerializer, UniversityRetrieveSerializer,
                              OrgAdminListSerializer, OrgAdminRetrieveSerializer, CustomerListSerializer,
                              CustomerRetrieveSerializer, PermissionListSerializer, PermissionRetrieveSerializer,
                              PermissionGroupListSerializer, PermissionGroupRetrieveSerializer,
                              CustomerUPGListSerializer, CustomerUPGRetrieveSerializer, FeatureGroupListSerializer,
                              FeatureGroupRetrieveSerializer, FeatureListSerializer, FeatureRetrieveSerializer)
from core.forms import (UniversityForm, OrgAdminCreateForm, CustomerCreationForm, CustomerUPGForm, FeatureGroupForm,
                        FeatureForm, PermissionGroupForm, UserAuthenticationForm, UserChangePasswordForm,
                        UserResetPassword, GrantUserPermissionForm)


USER_LEVEL_MAP = {
    0: '游客',
    1: '在校生',
    2: '临校生',
    3: '毕业生',
    4: '赞助商',
    5: '黑名单',
}
