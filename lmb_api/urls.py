from django.conf.urls import url, patterns
from lmb_api.restful import lmb_api, s3_api, user_api

urlpatterns = patterns(
    '',
    url(r'feature-groups/$', lmb_api.FeatureGroupList.as_view(), name='feature-group-list'),
    url(r'feature-groups/(?P<pk>[0-9]+)/$', lmb_api.FeatureGroupDetail.as_view(), name='feature-group-retrieve'),
    url(r'feature-groups/create/$', lmb_api.create_update_feature_group, name='feature-group-creation'),
    url(r'feature-groups/update/(?P<pk>[0-9]+)/$', lmb_api.create_update_feature_group,
        name='feature-group-update'),

    url(r'features/$', lmb_api.FeatureList.as_view(), name='feature-list'),
    url(r'features/(?P<pk>[0-9]+)/$', lmb_api.FeatureDetail.as_view(), name='feature-retrieve'),
    url(r'features/create/$', lmb_api.create_update_feature, name='feature-creation'),
    url(r'features/update/(?P<pk>[0-9]+)/$', lmb_api.create_update_feature, name='feature-update'),

    url(r'permissions/$', lmb_api.PermissionList.as_view(), name='permission-list'),
    url(r'permissions/(?P<pk>[0-9]+)/$', lmb_api.PermissionRetrieve.as_view(), name='permission-retrieve'),

    url(r'permission-groups/$', lmb_api.PermissionGroupList.as_view(), name='permission-group-list'),
    url(r'permission-groups/(?P<pk>[0-9]+)/$', lmb_api.PermissionGroupRetrieve.as_view(),
        name='permission-group-retrieve'),
    url(r'permission-groups/create/$', lmb_api.create_update_permission_group, name='permission-group-creation'),
    url(r'permission-groups/update/(?P<pk>[0-9]+)/$', lmb_api.create_update_permission_group,
        name='permission-group-update'),

    url(r'universities/$', lmb_api.UniversityList.as_view(), name='university-list'),
    url(r'universities/(?P<pk>[0-9])+/$', lmb_api.UniversityRetrieve.as_view(), name='university-retrieve'),
    url(r'universities/create/$', lmb_api.create_update_university, name='university-creation'),
    url(r'universities/update/(?P<pk>[0-9])+/$', lmb_api.create_update_university, name='university-update'),

    url(r'org-admins/$', lmb_api.OrgAdminList.as_view(), name='org-admin-list'),
    url(r'org-admins/(?P<pk>[0-9]+)/$', lmb_api.OrgAdminRetrieve.as_view(), name='org-admin-retrieve'),
    url(r'org-admins/create/$', lmb_api.create_org_admin, name='org-admin-creation'),

    url(r'customers/$', lmb_api.CustomerList.as_view(), name='customer-list'),
    url(r'customers/(?P<pk>[0-9]+)/$', lmb_api.CustomerRetrieve.as_view(), name='customer-retrieve'),
    url(r'customers/create/$', lmb_api.create_customer, name='customer-creation'),

    url(r'customer-upg/$', lmb_api.CustomerUPGList.as_view(), name='customer-upg-list'),
    url(r'customer-upg/(?P<pk>[0-9]+)/$', lmb_api.CustomerUPGRetrieve.as_view(),
        name='customer-upg-retrieve'),
    url(r'customer-upg/create/$', lmb_api.create_update_customer_upg, name='customer-upg-creation'),
    url(r'customer-upg/update/$', lmb_api.create_update_customer_upg, name='customer-upg-update'),

    url(r'portal/image/upload/$', s3_api.upload_image, name='image-upload'),
    url(r'portal/wiki/upload/$', s3_api.upload_wiki, name='wiki-upload'),
    url(r'portal/keys/get/$', s3_api.get_items, name='get-keys'),
    url(r'portal/keys/delete/$', s3_api.delete_wiki, name='delete-keys'),

    url(r'portal/customer/signup/$', user_api.customer_signup, name='customer-signup'),
    url(r'portal/user/login/$', user_api.login, name='user-login'),
    url(r'portal/user/logout/$', user_api.logout, name='user-logout'),
    url(r'portal/user/change-password/$', user_api.change_password, name='change-password'),
    url(r'portal/user/reset-password/$', user_api.reset_password, name='reset-password'),
    url(r'portal/grant-perm-group/admin/$', user_api.grant_admin_permission_groups, name='org-admin-grant-permissions'),
)

