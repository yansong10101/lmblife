from django.db import models
from django.template.defaultfilters import slugify
from lmb_core.feature.models import Feature


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

    class Meta:
        db_table = 'lmb_model_permission'

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
    display_name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    is_org_admin = models.BooleanField(default=True)
    is_super_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_level = models.IntegerField(choices=USER_LEVEL, default=0)

    objects = models.Manager()
    permission_groups = PermissionGroupManager()

    class Meta:
        db_table = 'lmb_model_permission_group'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        super(PermissionGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.group_name

    def __unicode__(self):
        return self.__str__()
