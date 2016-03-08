from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from core.managers import (AbstractBaseUser, UniversityManager, FeatureGroupManager, FeatureManager, PermissionManager,
                           PermissionGroupManager, OrgAdminManager, CustomerManager, CustomerUPGManager)
from django.shortcuts import get_object_or_404


class University(models.Model):
    university_name = models.CharField(max_length=255)
    university_code = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50, blank=True)
    display_name = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    contact_email = models.EmailField(blank=True)
    support_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    official_website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    universities = UniversityManager()

    def __str__(self):
        return self.university_name

    def __unicode__(self):
        return self.__str__()

    def has_relationship(self):
        return self.is_active

    @classmethod
    def create(cls, **kwargs):
        university = cls.universities.create(**kwargs)
        return university


class FeatureGroup(models.Model):
    feature_name = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150, blank=True)
    description_wiki_key = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    feature_groups = FeatureGroupManager()

    def __str__(self):
        return self.feature_name

    @classmethod
    def create(cls, **kwargs):
        feature_group = cls.feature_groups.create(**kwargs)
        return feature_group


class Feature(models.Model):
    feature_group = models.ForeignKey(FeatureGroup, related_name='feature_group')
    feature_name = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150, blank=True)
    description_wiki_key = models.CharField(max_length=255, blank=True)
    # view_type = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    features = FeatureManager()

    def __str__(self):
        return self.feature_name

    @classmethod
    def create_feature(cls, **kwargs):
        """
            create new feature:
            1. add to permission
        """
        feature = cls.features.create(**kwargs)
        # create corresponding permissions based on feature
        Permission.permissions.create_permission(feature)
        return feature


class Permission(models.Model):
    """
        Only do insertion when create new features
    """

    PERMISSION_TYPE = (
        ('r', 'read only'),
        ('f', 'full access'),
    )

    feature = models.ForeignKey(Feature, related_name='feature_permission')
    permission_name = models.CharField(max_length=255)
    permission_type = models.CharField(choices=PERMISSION_TYPE, max_length=2, default='r')
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    permissions = PermissionManager()

    def __str__(self):
        return self.permission_name

    @classmethod
    def create(cls, feature, **kwargs):
        return cls.permissions.create_permission(feature, **kwargs)


class PermissionGroup(models.Model):
    """
        insert rows:
        1. org president grant sub admin users
    """
    USER_LEVEL = (
        (0, '游客'),
        (1, '在校生'),
        (2, '临校生'),
        (3, '毕业生'),
        (4, '赞助商'),
        (5, '黑名单'),
    )

    permission = models.ManyToManyField(Permission, related_name='group_permission')
    group_name = models.CharField(max_length=150)
    is_org_admin = models.BooleanField(default=True)
    is_super_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_level = models.IntegerField(choices=USER_LEVEL, default=0)

    objects = models.Manager()
    permission_groups = PermissionGroupManager()

    def __str__(self):
        return self.group_name

    def __unicode__(self):
        return self.__str__()

    @classmethod
    def create(cls, permission_list=None, **kwargs):
        permission_group = cls.permission_groups.create(**kwargs)
        if permission_list:
            for permission_id in permission_list:
                permission = Permission.permissions.get(pk=permission_id)
                if isinstance(permission, Permission):
                    permission_group.permission.add(permission)
        return permission_group

    @classmethod
    def update(cls, permission_group, permission_list):
        origin_permissions = permission_group.permission.all()

        # remove permissions which are in group but not in passed-in list
        for permission in origin_permissions:
            if permission.pk not in permission_list:
                permission_group.permission.remove(permission)

        # add permissions which are not in passed-in list
        for permission_id in permission_list:
            if not permission_group.permission.filter(pk=permission_id).exists():
                permission = get_object_or_404(Permission, pk=permission_id)
                permission_group.permission.add(permission)


class OrgAdmin(AbstractBaseUser):
    university = models.ForeignKey(University, related_name='org_admin_university')
    permission_group = models.ManyToManyField(PermissionGroup, related_name='org_permission_group')
    username = models.CharField(_('username'), max_length=50, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and @/./+/-/_ characters.'), 'invalid'),
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                            })
    email = models.EmailField(verbose_name='email address', max_length=255)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    last_login_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_president = models.BooleanField(default=False, editable=False)
    is_admin = models.BooleanField(default=False, editable=False)
    prior_level = models.IntegerField(default=0)

    objects = models.Manager()
    org_admins = OrgAdminManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.get_username()

    def get_short_name(self):
        return self.get_username()

    def __str__(self):
        return self.get_full_name()


class Customer(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    last_login_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, editable=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    student_id = models.CharField(max_length=50, blank=True)
    offer_number = models.CharField(max_length=255, blank=True)
    photo_url = models.CharField(max_length=150, blank=True)
    # is_email_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approval_level = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'

    objects = models.Manager()
    customers = CustomerManager()

    def has_name(self):
        if not self.first_name and not self.last_name:
            return True
        return False

    def get_full_name(self):
        if self.has_name():
            return self.first_name, self.last_name
        return self.email

    def get_short_name(self):
        if self.has_name():
            return self.first_name
        return self.email.split('@')[0]

    @property
    def is_staff(self):
        return self.is_admin

    def inactive_user(self):
        self.is_active = False
        self.save()

    def update_password(self, password):
        self.set_password(password)

    def __str__(self):
        return self.email


class CustomerUPG(models.Model):
    """
        CustomerUPG == Customer University Permission Group
        Keep records for customer permission group in university
    """
    customer = models.ForeignKey(Customer, related_name='customer_upg_customer')
    university = models.ForeignKey(University, related_name='customer_upg_university')
    permission_group = models.ForeignKey(PermissionGroup, null=True, blank=True,
                                         related_name='customer_upg_permission_group')
    grant_level = models.IntegerField(default=0, verbose_name='grant user level')
    apply_from_feature = models.ForeignKey(Feature, related_name='customer_upg_feature', null=True, blank=True)
    is_approve = models.NullBooleanField(null=True)
    admin_comment = models.TextField(blank=True)
    customer_comment = models.TextField(blank=True)
    # created_date = models.DateTimeField(auto_now_add=True, editable=False)
    # last_modified_date = models.DateTimeField(auto_now=True, editable=False)

    objects = models.Manager()
    customer_upg = CustomerUPGManager()

    def __str__(self):
        return '-'.join((str(self.customer), str(self.university), str(self.permission_group), str(self.grant_level)))


class CustomerMessage(models.Model):
    customer = models.ManyToManyField(Customer, related_name='customer_message')
    admin = models.ManyToManyField(OrgAdmin, related_name='org_admin_message')
    # created_date = models.DateTimeField(auto_now_add=True, editable=False)
    # last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    type = models.CharField(max_length=255, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return '-'.join([self.subject, self.message])
