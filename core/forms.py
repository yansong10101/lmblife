from django import forms
from core.models import (University, OrgAdmin, Customer, CustomerUPG, FeatureGroup, Feature, PermissionGroup,
                         UniversityAdditionalAttributes)
from lmb_api.utils import get_cached_user, check_request_user_role, get_cached_user_by_email
from django.shortcuts import get_object_or_404


USER_BACKEND = 'django.contrib.auth.backends.ModelBackend'
FORM_ERROR_CODE_MAP = {
    1: 'invalid',
    2: 'missing arg',
    3: 'not match',
    4: 'unauthorized',
}


class UniversityForm(forms.ModelForm):

    class Meta:
        model = University
        fields = ('handle', 'university_code', 'display_name', )


class UniversityAdditionalAttributesForm(forms.ModelForm):
    token = forms.CharField(label='token', required=False)
    slug = forms.CharField(label='slug', required=True)

    class Meta:
        model = UniversityAdditionalAttributes
        fields = ('attribute_name', 'attribute_value', 'attribute_long_value', )

    def validate_permission(self):
        cached_data = get_cached_user(self.cleaned_data.get('token'))
        university = get_object_or_404(University, slug_name=self.cleaned_data.get('slug'))
        if cached_data['university_id'] != university.pk or not check_request_user_role(cached_data,
                                                                                        ['president', 'admin']):
            raise forms.ValidationError('User has no permission !', code=FORM_ERROR_CODE_MAP[4])
        return True

    def save(self, commit=True):
        if self.validate_permission():
            university = get_object_or_404(University, slug_name=self.cleaned_data.get('slug'))
            uni_attr = \
                UniversityAdditionalAttributes.objects.filter(university=university,
                                                              attribute_name=self.cleaned_data.get('attribute_name'))
            if uni_attr.count() == 1:
                # already exists
                attr_obj = uni_attr[0]
                attr_obj.attribute_name = self.cleaned_data.get('attribute_name')
                attr_obj.attribute_value = self.cleaned_data.get('attribute_value')
                attr_obj.attribute_long_value = self.cleaned_data.get('attribute_long_value')
                attr_obj.save()
            elif uni_attr.count() == 0:
                uni_add_attr = UniversityAdditionalAttributes()
                uni_add_attr.university = university
                uni_add_attr.attribute_name = self.cleaned_data.get('attribute_name')
                uni_add_attr.attribute_value = self.cleaned_data.get('attribute_value')
                uni_add_attr.attribute_long_value = self.cleaned_data.get('attribute_long_value')
                # super(UniversityAdditionalAttributesForm, self).save()
                uni_add_attr.save()
            else:
                raise forms.ValidationError('Duplicated University Additional Attributes Error!',
                                            code=FORM_ERROR_CODE_MAP[1])


class CustomerCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('email', 'first_name', 'last_name', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match !')
        return password2

    def save(self, commit=True):
        user = super(CustomerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class OrgAdminCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = OrgAdmin
        fields = ('university', 'username', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match !')
        return password2

    def save(self, commit=True):
        user = super(OrgAdminCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomerUPGForm(forms.ModelForm):
    token = forms.CharField(label='token', required=True)
    customer = forms.CharField(required=False, label='customer')
    university_slug = forms.CharField(label='university slug', required=True)

    class Meta:
        model = CustomerUPG
        fields = ('permission_group', 'is_approved', 'admin_comment', 'customer_comment', 'apply_from_feature',
                  'grant_level', 'apply_level', )

    def get_customer(self, cached_data):
        if check_request_user_role(cached_data, ('customer', )):
            return get_object_or_404(Customer, pk=int(cached_data['user_id']))
        else:
            return get_object_or_404(Customer, email=self.cleaned_data.get('customer'))

    @staticmethod
    def validate_existing(customer, university):
        customer_in_university = CustomerUPG.customer_upg.all().filter(customer=customer, university=university) or None
        if customer_in_university and customer_in_university.count() > 1:
            raise forms.ValidationError('Create CustomerUPG Exception: should be unique!' + str(customer_in_university),
                                        code=FORM_ERROR_CODE_MAP[1])
        if customer_in_university and customer_in_university.count() == 1:
            return True
        return False

    def create_customer_upg(self):
        cached_data = get_cached_user(self.cleaned_data.get('token'))
        customer = self.get_customer(cached_data)
        university = get_object_or_404(University, slug_name=self.cleaned_data.get('university_slug'))
        if self.validate_existing(customer, university):
            raise forms.ValidationError('Already exist !', code=FORM_ERROR_CODE_MAP[1])
        customer_comment = self.cleaned_data.get('customer_comment')
        feature = self.cleaned_data.get('apply_from_feature')
        apply_level = self.cleaned_data.get('apply_level') or 0
        customer_upg = CustomerUPG(customer=customer, university=university, customer_comment=customer_comment,
                                   apply_from_feature=feature, apply_level=apply_level)
        customer_upg.save()
        return customer_upg

    def update_customer_upg(self):
        cached_data = get_cached_user(self.cleaned_data.get('token'))
        customer = self.get_customer(cached_data)
        university = get_object_or_404(University, slug_name=self.cleaned_data.get('university_slug'))
        if cached_data['university_id'] != university.pk:
            raise forms.ValidationError('User has no permission !', code=FORM_ERROR_CODE_MAP[4])
        permission_group = self.cleaned_data.get('permission_group')
        is_approved = self.cleaned_data.get('is_approved')
        admin_comment = self.cleaned_data.get('admin_comment')
        grant_level = self.cleaned_data.get('grant_level') or None
        customer_in_university = CustomerUPG.customer_upg.all().filter(customer=customer.pk,
                                                                       university=university) or None
        if not permission_group or not is_approved or not admin_comment or not customer:
            raise forms.ValidationError('Required Field [customer, permission_group, is_approved, admin_comment, ] !',
                                        code=FORM_ERROR_CODE_MAP[2])
        if customer_in_university is None or customer_in_university.count() > 1:
            raise forms.ValidationError('Update CustomerUPG Exception: should be unique!' + str(customer_in_university),
                                        code=FORM_ERROR_CODE_MAP[1])
        elif customer_in_university.count() == 1:
            customer_upg = customer_in_university[0]
            customer_upg.permission_group = permission_group
            customer_upg.grant_level = grant_level or permission_group.user_level
            customer_upg.is_approved = is_approved
            customer_upg.admin_comment = admin_comment
            customer_upg.save()
            return customer_upg


class UserAuthenticationForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    token = forms.CharField(label='Token', required=False)

    def authenticate(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        token = self.cleaned_data.get('token') or None
        user = Customer.customers.get_auth_customer(username) or OrgAdmin.org_admins.get_auth_admin(username)
        if user and user.check_password(password):
            user.backend = USER_BACKEND
            return user, token
        return None, None


class UserChangePasswordForm(forms.Form):
    code = forms.CharField(required=True)
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    @staticmethod
    def get_user(cached_data):
        if check_request_user_role(cached_data, ('customer', )):
            return get_object_or_404(Customer, pk=int(cached_data['user_id']))
        else:
            return get_object_or_404(OrgAdmin, pk=int(cached_data['user_id']))

    @staticmethod
    def authenticate(user, old_password):
        if user and user.check_password(old_password):
            user.backend = USER_BACKEND
            return True
        return False

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match !')
        return password2

    def set_password(self):
        old_password = self.cleaned_data.get('old_password')
        cached_data = get_cached_user(self.cleaned_data.get('code'))
        if not cached_data:
            raise forms.ValidationError('Unauthorized User !')
        user = UserChangePasswordForm.get_user(cached_data)
        password = self.clean_password2()
        if UserChangePasswordForm.authenticate(user, old_password) and password:
            user.set_password(password)
            user.save()
            return user
        return None


class UserResetPassword(forms.Form):
    code = forms.CharField(required=True)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match !')
        return password2

    def reset_password(self):
        user = get_cached_user_by_email(self.cleaned_data.get('code'))
        password = self.clean_password2()
        if user and password:
            user.backend = USER_BACKEND
            user.set_password(password)
            user.save()
            return user
        return None


class UserForgotPassword(forms.Form):
    username = forms.CharField(label='Username')

    def get_user(self):
        username = self.cleaned_data.get('username')
        return Customer.customers.get_auth_customer(username) or None


class GrantUserPermissionForm(forms.Form):
    username = forms.CharField(label='Username')

    def authenticate(self):
        username = self.cleaned_data.get('username')
        user = Customer.customers.get_auth_customer(username) or OrgAdmin.org_admins.get_auth_admin(username)
        if user:
            user.backend = USER_BACKEND
            return user
        return None


class FeatureGroupForm(forms.ModelForm):
    class Meta:
        model = FeatureGroup
        fields = ['feature_name', 'display_name', 'description_wiki_key', 'description', ]


class FeatureForm(forms.ModelForm):

    class Meta:
        model = Feature
        fields = ['feature_group', 'feature_name', 'display_name', 'description_wiki_key', 'description', 'view_type', ]


class PermissionGroupForm(forms.ModelForm):
    class Meta:
        model = PermissionGroup
        fields = ['group_name', 'is_org_admin', 'user_level', ]


class UserAvatarFileForm(forms.Form):
    token = forms.CharField()
    file = forms.FileField()

    def get_user(self):
        cached_data = get_cached_user(self.cleaned_data.get('token'))
        user = Customer.customers.get_auth_customer(cached_data['username']) or None
        if not cached_data or not user:
            raise forms.ValidationError('Unauthorized User !')
        return user

    def make_avatar_s3_key_prefix(self):
        user = self.get_user()
        return '{}/{}/'.format(user.pk, 'avatar')

    def update_user_avatar_key(self, bucket, s3_key):
        user = self.get_user()
        user.avatar_url = '{}/{}/{}'.format('https://s3-us-west-2.amazonaws.com', bucket, s3_key)
        user.save()
        return user.avatar_url
