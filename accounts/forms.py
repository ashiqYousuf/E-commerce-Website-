from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , UsernameField , PasswordResetForm , SetPasswordForm , PasswordChangeForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from .models import Address


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,'class':'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    )



class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['locality','city','state','pincode']
        widgets={
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'pincode':forms.NumberInput(attrs={'class':'form-control'}),
        }
        error_messages={
            'locality':{'required':'This field is required *'},
            'city':{'required':'This field is required *'},
            'state':{'required':'This field is required *'},
            'pincode':{'required':'This field is required *'},
        }


class CustomSetPasswordForm(SetPasswordForm):
        """
        A form that lets a user change set their password without entering the old
        password
        """
        error_messages = {
            'password_mismatch': _('The two password fields didn’t match.'),
        }
        new_password1 = forms.CharField(
            label=_("New password"),
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
            strip=False,
            help_text=password_validation.password_validators_help_text_html(),
        )
        new_password2 = forms.CharField(
            label=_("New password confirmation"),
            strip=False,
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        )




class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email','class':'form-control'})
    )


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels={
            'username':'Username (unique)',
            'email':'Email ID',
        }
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }
        
class LoginForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(label='Username',widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control'}),
    )