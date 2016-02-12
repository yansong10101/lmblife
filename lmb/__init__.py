from lmb.models import Customer, University, OrgAdmin, CustomerUPG, FeatureGroup, Feature, Permission, PermissionGroup

from lmb.serializers import (Customer, University, OrgAdmin, CustomerUPG, FeatureGroup, Feature, Permission,
                             PermissionGroup, UniversityListSerializer, UniversityRetrieveSerializer,
                             OrgAdminListSerializer, OrgAdminRetrieveSerializer, CustomerListSerializer,
                             CustomerRetrieveSerializer, PermissionListSerializer, PermissionRetrieveSerializer,
                             PermissionGroupListSerializer, PermissionGroupRetrieveSerializer,
                             CustomerUPGListSerializer, CustomerUPGRetrieveSerializer, FeatureGroupListSerializer,
                             FeatureGroupRetrieveSerializer, FeatureListSerializer, FeatureRetrieveSerializer)
from lmb.forms import (UniversityForm, OrgAdminCreateForm, CustomerCreationForm, CustomerUPGForm, FeatureGroupForm,
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
