from django.db import models
from django.contrib.auth.models import BaseUserManager


class UniversityManager(models.Manager):
    """
        create new university:
        1. with all default features (recommend only toggle existing features)
        2. create a super user (president)
        3. grant all permissions to president
        4. can create group
    """

    def get_queryset(self, is_active=True):
        return super(UniversityManager, self).get_queryset().filter(is_active=is_active)


class FeatureGroupManager(models.Manager):
    """
        create new feature group:
        1. add to administration permission model
    """

    def get_queryset(self, is_active=True, **kwargs):
        return super(FeatureGroupManager, self).get_queryset().filter(is_active=is_active, **kwargs)


class FeatureManager(models.Manager):
    """
        create new feature:
        1. add to administration permission model
    """

    def get_queryset(self, is_active=True):
        return super(FeatureManager, self).get_queryset().filter(is_active=is_active)


class PermissionManager(models.Manager):

    PERMISSION_NAME_SUFFIX = {
        'r': 'ReadOnlyAccess',
        'f': 'FullAccess',
    }

    def create_permission(self, feature, **kwargs):
        feature_name = feature.feature_name
        read_only = self.create(feature=feature, permission_name=self.make_permission_name(feature_name, 'r'),
                                permission_type='r', **kwargs)
        full_access = self.create(feature=feature, permission_name=self.make_permission_name(feature_name, 'f'),
                                  permission_type='f', **kwargs)
        return read_only, full_access

    def make_permission_name(self, feature_name, permission_type):
        return ''.join(feature_name.title().split()) + self.PERMISSION_NAME_SUFFIX[permission_type]

    def get_queryset(self, **kwargs):
        return super(PermissionManager, self).get_queryset().filter(is_active=True, **kwargs)


class PermissionGroupManager(models.Manager):

    def get_queryset(self, is_active=True, **kwargs):
        return super(PermissionGroupManager, self).get_queryset().filter(is_active=is_active, **kwargs)


class OrgAdminQuerySet(models.QuerySet):

    def org_president(self, **kwargs):
        return self.filter(is_president=True, is_active=True, **kwargs)

    def org_admin(self, **kwargs):
        return self.filter(is_president=False, is_active=True, **kwargs)

    def get_org_admin_by_username(self, username):
        org_admin_list = self.filter(is_active=True, username=username)
        if org_admin_list:
            return org_admin_list[0]
        return None


class OrgAdminManager(BaseUserManager):

    def get_queryset(self):
        return OrgAdminQuerySet(self.model, using=self._db).filter(is_active=True)

    def org_president(self, **kwargs):
        return self.get_queryset().org_president(**kwargs)

    def org_admin(self, **kwargs):
        return self.get_queryset().org_admin(**kwargs)

    def get_auth_admin(self, username):
        return self.get_queryset().get_org_admin_by_username(username)


class CustomerQuerySet(models.QuerySet):

    def get_customers(self, is_active=True, **kwargs):
        return self.filter(is_active=is_active, **kwargs)

    def unauthorized_user(self):
        return self.get_customers(approval_level=0)

    def authorized_user(self):
        return self.get_customers(approval_level=1)

    def alumni(self):
        return self.get_customers(approval_level=2)

    def get_customer_by_email(self, email):
        customer_list = self.get_customers(email=email)
        if customer_list:
            return customer_list[0]
        return None


class CustomerManager(BaseUserManager):

    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def get_customer(self, **kwargs):
        return self.get_customer(**kwargs)

    def unauthorized_user(self):
        return self.get_queryset().unauthorized_user()

    def authorized_user(self):
        return self.get_queryset().authorized_user()

    def alumni(self):
        return self.get_queryset().alumni()

    def get_auth_customer(self, email):
        return self.get_queryset().get_customer_by_email(email)


class CustomerUPGManager(models.Manager):

    def get_queryset(self, **kwargs):
        return super(CustomerUPGManager, self).get_queryset().filter(**kwargs)
