from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomerQuerySet(models.QuerySet):

    def get_customers(self, is_active=True, **kwargs):
        return self.filter(is_active=is_active, **kwargs)

    def get_customer_by_email(self, email):
        return self.get(email__exact=email)


class CustomerManager(BaseUserManager):

    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def get_customer_by_email(self, email):
        return self.get_queryset().get_customer_by_email(email)


class Customer(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    last_login_date = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=16, blank=True)
    address_1 = models.CharField(max_length=225, blank=True)
    address_2 = models.CharField(max_length=225, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    avatar_url = models.CharField(max_length=225, blank=True)

    USERNAME_FIELD = 'email'

    objects = models.Manager()
    customers = CustomerManager()

    class Meta:
        db_table = 'lmb_model_customer'

    def has_name(self):
        if self.first_name and self.last_name:
            return True
        return False

    def get_full_name(self):
        if self.has_name():
            return '{} {}'.format(self.first_name, self.last_name)
        return self.email

    def get_short_name(self):
        if self.has_name():
            return self.first_name
        return self.email.split('@')[0]

    def update_password(self, password):
        self.set_password(password)

    def __str__(self):
        return self.get_full_name()

    def __getattr__(self, item):
        return self.__dict__[item]

    def make_attr_dict(self, attr_list):
        attr_dict = dict()
        for attr in attr_list:
            attr_dict[attr] = self.__getattr__(attr)
        return attr_dict
