from .models import University, OrgAdmin, Customer, CustomerUPG, FeatureGroup, Feature, PermissionGroup
from django import forms


USER_BACKEND = 'django.contrib.auth.backends.ModelBackend'


class UniversityForm(forms.ModelForm):

    class Meta:
        model = University
        fields = ('university_name', 'university_code', )


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

    class Meta:
        model = CustomerUPG
        fields = ('customer', 'university', 'permission_group', 'approval_comment', )

    def validate_existing(self):
        customer = self.cleaned_data.get('customer')
        university = self.cleaned_data.get('university')
        customer_upg_list = CustomerUPG.objects.all().filter(university=university)
        for customer_item in customer_upg_list:
            if customer.pk == customer_item.pk:
                return True
        return False

    def update_customer_university_group(self):
        customer = self.cleaned_data.get('customer')
        university = self.cleaned_data.get('university')
        permission_group = self.cleaned_data.get('permission_group')
        customer_in_university = CustomerUPG.customer_upg.all().filter(customer=customer, university=university) or None
        if customer_in_university is None or customer_in_university.count() > 1:
            # TODO : write validation
            raise Exception('Unknown object exception: !' + customer_in_university)
        elif customer_in_university.count() == 1:
            customer_in_university[0].permission_group = permission_group
            customer_in_university[0].grant_level = permission_group.user_level
            customer_in_university[0].save()
        return customer_in_university[0]


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
        return None


class UserChangePasswordForm(forms.Form):
    username = forms.CharField(label='Username')
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match !')
        return password2

    def authenticate(self):
        username = self.cleaned_data.get('username')
        old_password = self.cleaned_data.get('old_password')
        user = Customer.customers.get_auth_customer(username) or OrgAdmin.org_admins.get_auth_admin(username)
        if user and user.check_password(old_password):
            user.backend = USER_BACKEND
            return user
        return None

    def set_password(self):
        user = self.authenticate()
        password = self.clean_password2()
        if user and password:
            user.set_password(password)
            user.save()
            return user
        return None


class UserResetPassword(forms.Form):
    username = forms.CharField(label='Username')
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match !')
        return password2

    def get_user(self):
        username = self.cleaned_data.get('username')
        user = Customer.customers.get_auth_customer(username) or OrgAdmin.org_admins.get_auth_admin(username)
        if user:
            user.backend = USER_BACKEND
            return user
        return None

    def reset_password(self):
        user = self.get_user()
        password = self.clean_password2()
        if user and password:
            user.set_password(password)
            user.save()
            return user
        return None


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
        fields = ['feature_group', 'feature_name', 'display_name', 'description_wiki_key', 'description', ]


class PermissionGroupForm(forms.ModelForm):
    class Meta:
        model = PermissionGroup
        fields = ['group_name', 'is_org_admin', 'user_level', ]
