from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from .models import User


class UserSignupForm(forms.ModelForm):
    """
    Signup form class
    """
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(
        label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(
        label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(
        label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(
        label='confirm_password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
  
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password','confirm_password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Signup'))


class UserLoginForm(AuthenticationForm):
    """
    Login Form class
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', "placeholder": "Email Address"}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('email', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_action = 'login'
        self.helper.field_class = 'form-control'
        self.helper.form_show_errors = True

        self.helper.layout.append(
            Submit('login', 'Login', css_class='btn btn-warning w-100'))



class ClientSignupForm(forms.ModelForm):
    """
    Signup form class
    """
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'input email address e.g. john.doe@email.com'}))
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(
        label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(
        label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    date_of_birth = forms.DateTimeField(label='Date of Birth', widget=forms.TextInput(
        attrs={'type': 'date','placeholder': 'Date'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username', 'password','date_of_birth','is_client')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Signup'))


class WriterSignupForm(forms.ModelForm):
    """
    Signup form class
    """
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'input email e.g. Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(
        label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(
        label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('first_name', 'username','last_name',
        'phone','additional_phone','email','time_zone','night_calls',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Signup'))


class UserUpdateProfileForm(forms.ModelForm):
    """
    update profile form class
    """
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email Address', 'class':'form-control'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class':'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class':'form-control'}))
    # username = forms.CharField(
    #     label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    country = forms.CharField( label='Country', widget=forms.TextInput(
        attrs={'placeholder': 'Country', 'class':'form-control'}))
    time_zone = forms.CharField( label='Time Zone', widget=forms.TextInput(
        attrs={'placeholder': 'Time Zone', 'class':'form-control'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(
        attrs={'placeholder': 'Phone', 'class': 'form-control'}))
    additional_phone = forms.CharField(label='Additional Phone', widget=forms.TextInput(
        attrs={'placeholder': 'Additional Phone', 'class': 'form-control'}))
    night_calls =forms.Select(attrs={'id':'night_calls','placeholder': 'Night Calls',})
    city = forms.CharField(label='City', widget=forms.TextInput(
        attrs={'placeholder': 'City', 'class': 'form-control'}))
    address = forms.CharField(label='Adress', widget=forms.TextInput(
        attrs={'placeholder': 'Address', 'class': 'form-control'}))
    zip_code = forms.CharField(label='Zip Code', widget=forms.TextInput(
        attrs={'placeholder': 'Zip Code', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'time_zone','country','phone','additional_phone','night_calls','city','address','zip_code',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Update'))

class UpdateTimezoneForm(forms.ModelForm):
    """
    update timezone form class
    """
    time_zone = forms.CharField( label='Time Zone', widget=forms.TextInput(
        attrs={'placeholder': 'Time Zone', 'class':'form-control'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(
        attrs={'placeholder': 'Country', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ( 'time_zone','country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Update'))