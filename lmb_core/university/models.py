from django.db import models
from django.template.defaultfilters import slugify


class UniversityQueryset(models.QuerySet):

    def get_universities(self, is_active=True, **kwargs):
        return self.filter(is_active=is_active, **kwargs)

    def get_university_by_handle(self, handle):
        return self.get(handle__exact=handle)

    def get_university_by_slug(self, slug):
        return self.get(slug__exact=slug)


class UniversityManager(models.Manager):

    def get_queryset(self):
        return UniversityQueryset(self.model, using=self._db)

    def get_by_slug(self, slug):
        return self.get_queryset().get_university_by_slug(slug)


class University(models.Model):
    handle = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    display_name = models.CharField(max_length=500, blank=True)
    alternative_name = models.CharField(max_length=500, blank=True)
    university_code = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)
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

    class Meta:
        db_table = 'lmb_model_university'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.handle)
        super(University, self).save(*args, **kwargs)

    def __str__(self):
        return self.handle

    def __unicode__(self):
        return self.__str__()


class UniversityAdditionalAttributes(models.Model):
    university = models.ForeignKey(University, related_name='university')
    attribute_name = models.CharField(max_length=255)
    attribute_value = models.CharField(max_length=255, blank=True)
    attribute_long_value = models.TextField(blank=True)

    class Meta:
        db_table = 'lmb_model_university_additional_attributes'

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.university.handle,
                                       self.attribute_name,
                                       self.attribute_value,
                                       self.attribute_long_value)

    def __unicode__(self):
        return self.__str__()
