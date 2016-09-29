from django.db import models
from django.template.defaultfilters import slugify


class FeatureGroupQuerySet(models.QuerySet):

    def get_feature_groups(self, is_active=True, **kwargs):
        return self.filter(is_active=is_active, **kwargs)


class FeatureGroupManager(models.Manager):

    def get_queryset(self):
        return FeatureGroupQuerySet(self.model, using=self._db)


class FeatureQuerySet(models.QuerySet):

    def get_features(self, is_active=True, **kwargs):
        return self.filter(is_active=is_active, **kwargs)

    def get_feature_and_group_by_handle(self, handle):
        return self.select_related('feature_group').get(handle__exact=handle)


class FeatureManager(models.Manager):

    def get_queryset(self):
        return FeatureQuerySet(self.model, using=self._db)

    def get_feature_and_group_by_handle(self, handle):
        return self.get_queryset()


class FeatureGroup(models.Model):
    feature_group_name = models.CharField(max_length=200, unique=True)
    display_name = models.CharField(max_length=255, blank=True)
    alternative_name = models.CharField(max_length=255, blank=True)
    description_wiki_key = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    feature_groups = FeatureGroupManager()

    class Meta:
        db_table = 'lmb_model_feature_group'

    def __str__(self):
        return self.feature_group_name


class Feature(models.Model):
    feature_group = models.ForeignKey(FeatureGroup, related_name='feature_group')
    feature_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, blank=True)
    display_name = models.CharField(max_length=255, blank=True)
    alternative_name = models.CharField(max_length=255, blank=True)
    description_wiki_key = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    view_type = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    features = FeatureManager()

    class Meta:
        db_table = 'lmb_model_feature'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.feature_name)
        super(Feature, self).save(*args, **kwargs)

    # @models.permalink
    # def get_absolute_url(self):
    #     return 'api:feature-slug', (self.slug, self.pk)

    def __str__(self):
        return self.feature_name
