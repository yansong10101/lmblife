from django import forms
from lmb_core.customer.models import Customer
from lmb_core.customer.utils import set_customer_to_cache

_USER_BACKEND = 'django.contrib.auth.backends.ModelBackend'


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
        customer = super(CustomerCreationForm, self).save(commit=False)
        customer.set_password(self.cleaned_data['password1'])
        if commit:
            customer.save()
        return customer


class CustomerAuthenticationForm(forms.Form):
    """
    WE DO NOT NEED 'TOKEN' IN LOGIN ACTION, BUT THE HEADER ALWAYS NEED TO CHECK 'TOKEN' IN PURPOSE OF API CALLS
    """
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def authenticate(self, token=None):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        customer = Customer.customers.get_customer_by_email(email)
        if customer and customer.check_password(password):
            customer.backend = _USER_BACKEND
            token = set_customer_to_cache(token, customer)
            return customer, token
        return None, None


class CustomerChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    auth_token = forms.CharField(label='token')

    def get_customer(self):
        token = self.cleaned_data.get('auth_token')
        print(token)
        return token

    # @staticmethod
    # def authenticate(user, old_password):
    #     if user and user.check_password(old_password):
    #         user.backend = _USER_BACKEND
    #         return True
    #     return False
    #
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError('Passwords do not match !')
    #     return password2
    #
    # def set_password(self):
    #     old_password = self.cleaned_data.get('old_password')
    #     cached_data = get_cached_user(self.cleaned_data.get('token'))
    #     if not cached_data:
    #         raise forms.ValidationError('Unauthorized User ! User may already logout, no token found !')
    #     user = UserChangePasswordForm.get_user(cached_data)
    #     password = self.clean_password2()
    #     if UserChangePasswordForm.authenticate(user, old_password) and password:
    #         user.set_password(password)
    #         user.save()
    #         return user
    #     return None


# class CustomerResetPassword(forms.Form):
#     code = forms.CharField(required=True)
#     password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError('Passwords do not match !')
#         return password2
#
#     def reset_password(self):
#         user = get_cached_user_by_email(self.cleaned_data.get('code'))
#         password = self.clean_password2()
#         if user and password:
#             user.backend = USER_BACKEND
#             user.set_password(password)
#             user.save()
#             return user
#         return None


class CustomerForgotPassword(forms.Form):
    email = forms.CharField(label='Email')

    def get_user(self):
        email = self.cleaned_data.get('email')
        return Customer.customers.get_customer_by_email(email)
