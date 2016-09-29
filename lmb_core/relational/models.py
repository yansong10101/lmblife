from django.db import models
from lmb_core.customer.models import Customer
from lmb_core.university.models import University
from lmb_core.permission.models import PermissionGroup


class CustomerUPGQuerySet(models.QuerySet):

    def get_customer_upg(self, **kwargs):
        return self.filter(**kwargs)

    def get_by_university(self, university):
        return self.filter(university=university)

    def get_by_customer(self, customer):
        return self.filter(customer=customer)

    def get_by_permission_group(self, permission_group):
        return self.filter(permission_group=permission_group)


class CustomerUPGManager(models.Manager):

    def get_queryset(self):
        return CustomerUPGQuerySet(self.model, using=self._db)

    def get_by_university(self, university):
        return self.get_queryset().get_by_university(university)

    def get_by_customer(self, customer):
        return self.get_queryset().get_by_customer(customer)

    def get_by_permission_group(self, permission_group):
        return self.get_queryset().get_by_permission_group(permission_group)


class CustomerUPG(models.Model):
    """
        CustomerUPG == Customer University Permission Group
        Keep records for customer permission group in university
    """
    customer = models.ForeignKey(Customer, related_name='customer_upg_customer')
    university = models.ForeignKey(University, related_name='customer_upg_university')
    permission_group = models.ForeignKey(PermissionGroup, null=True, blank=True,
                                         related_name='customer_upg_permission_group')
    grant_level = models.IntegerField(default=0, verbose_name='grant user level', blank=True)
    apply_level = models.IntegerField(default=0, verbose_name='apply user level', blank=True)
    is_approved = models.NullBooleanField(null=True)
    admin_comment = models.TextField(blank=True)
    customer_comment = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False, null=True)

    objects = models.Manager()
    customer_upg = CustomerUPGManager()

    class Meta:
        """
        One Customer should have only one role per University, make both unique together.
        """
        unique_together = ('customer', 'university', )

    def key_name(self):
        return '-'.join((str(self.customer), str(self.university), str(self.permission_group), str(self.grant_level)))

    def __str__(self):
        return self.key_name()
