from django.conf.urls import url, patterns
from lmb_api.restful import core_api, s3_api, user_api, weipost_api

# LMB Core APIs
urlpatterns = patterns(
    '',
    url(r'feature-groups/$', core_api.FeatureGroupList.as_view(), name='feature-group-list'),
    url(r'feature-groups/(?P<pk>[0-9]+)/$', core_api.FeatureGroupDetail.as_view(), name='feature-group-retrieve'),
    url(r'feature-groups/create/$', core_api.create_update_feature_group, name='feature-group-creation'),
    url(r'feature-groups/update/(?P<pk>[0-9]+)/$', core_api.create_update_feature_group,
        name='feature-group-update'),

    url(r'features/$', core_api.FeatureList.as_view(), name='feature-list'),
    url(r'features/(?P<pk>[0-9]+)/$', core_api.FeatureDetail.as_view(), name='feature-retrieve'),
    url(r'features/create/$', core_api.create_update_feature, name='feature-creation'),
    url(r'features/update/(?P<pk>[0-9]+)/$', core_api.create_update_feature, name='feature-update'),

    url(r'permissions/$', core_api.PermissionList.as_view(), name='permission-list'),
    url(r'permissions/(?P<pk>[0-9]+)/$', core_api.PermissionRetrieve.as_view(), name='permission-retrieve'),

    url(r'permission-groups/$', core_api.PermissionGroupList.as_view(), name='permission-group-list'),
    url(r'permission-groups/(?P<pk>[0-9]+)/$', core_api.PermissionGroupRetrieve.as_view(),
        name='permission-group-retrieve'),
    url(r'permission-groups/create/$', core_api.create_update_permission_group, name='permission-group-creation'),
    url(r'permission-groups/update/(?P<pk>[0-9]+)/$', core_api.create_update_permission_group,
        name='permission-group-update'),

    url(r'universities/$', core_api.UniversityList.as_view(), name='university-list'),
    url(r'universities/(?P<pk>[0-9])+/$', core_api.UniversityRetrieve.as_view(), name='university-retrieve'),
    url(r'universities/create/$', core_api.create_update_university, name='university-creation'),
    url(r'universities/update/(?P<pk>[0-9])+/$', core_api.create_update_university, name='university-update'),

    url(r'org-admins/$', core_api.OrgAdminList.as_view(), name='org-admin-list'),
    url(r'org-admins/(?P<pk>[0-9]+)/$', core_api.OrgAdminRetrieve.as_view(), name='org-admin-retrieve'),
    url(r'org-admins/create/$', core_api.create_org_admin, name='org-admin-creation'),

    url(r'customers/$', core_api.CustomerList.as_view(), name='customer-list'),
    url(r'customers/(?P<pk>[0-9]+)/$', core_api.CustomerRetrieve.as_view(), name='customer-retrieve'),
    url(r'customers/create/$', core_api.create_customer, name='customer-creation'),

    url(r'customer-upg/$', core_api.CustomerUPGList.as_view(), name='customer-upg-list'),
    url(r'customer-upg/(?P<pk>[0-9]+)/$', core_api.CustomerUPGRetrieve.as_view(),
        name='customer-upg-retrieve'),
    # "create_update_customer_upg" is used by customer and admin portal to apply and grant
    # url(r'customer-upg/create/$', core_api.create_update_customer_upg, name='customer-upg-creation'),
    # url(r'customer-upg/update/$', core_api.create_update_customer_upg, name='customer-upg-update'),
)

# User Portals
urlpatterns += patterns(
    '',
    url(r'portal/customer/signup/$', user_api.customer_signup, name='customer-signup'),
    url(r'portal/user/login/$', user_api.login, name='user-login'),
    url(r'portal/user/logout/$', user_api.logout, name='user-logout'),
    url(r'portal/user/change-password/$', user_api.change_password, name='change-password'),
    url(r'portal/user/reset-password/$', user_api.reset_password, name='reset-password'),
    url(r'portal/customer-permission/apply/$', user_api.create_update_customer_upg, name='customer-upg-create'),
    url(r'portal/refresh-cache/user-cache/$', user_api.refresh_user_cache, name='refresh-user-cache'),
    url(r'portal/email-token-verification/$', user_api.email_token_verification, name='user-email-token-verification'),
)

# Org Admin Portals
urlpatterns += patterns(
    '',
    url(r'portal/grant-perm-group/admin/$', user_api.grant_admin_permission_groups, name='org-admin-grant-permissions'),
    url(r'portal/grant-perm-group/customer/$', user_api.create_update_customer_upg, name='customer-upg-grant'),
)

# LMB Content APIs
#
# Wiki APIs
urlpatterns += patterns(
    '',
    url(r'portal/image/upload/$', s3_api.upload_image, name='image-upload'),
    url(r'portal/wiki/upload/$', s3_api.upload_wiki, name='wiki-upload'),
    url(r'portal/keys/get/$', s3_api.get_items, name='get-keys'),
    url(r'portal/keys/delete/$', s3_api.delete_wiki, name='delete-keys'),
)

# WeiPost APIs
urlpatterns += patterns(
    '',
    url(r'content/wei-post/list-post/$', weipost_api.JieJiPostList.as_view(), name='jie-ji-post-list'),
    url(r'content/wei-post/(?P<pk>[0-9]+)/get/$', weipost_api.JieJiPostRetrieve.as_view(), name='jie-ji-post-get'),

    url(r'content/wei-comment/list-comment/$', weipost_api.JieJiCommentList.as_view(), name='jie-ji-comment-list'),
    url(r'content/wei-comment/(?P<pk>[0-9]+)/get/$', weipost_api.JieJiCommentRetrieve.as_view(),
        name='jie-ji-comment-get'),
)
