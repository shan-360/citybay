from django import forms
from .models import Search, User, Registration, RATE_CHOICES, RateCity


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['search_address']
        labels = {
            'search_address': 'City',
        }


class RegistrationForm(forms.ModelForm):
    reg_pwd = forms.CharField(widget=forms.PasswordInput(), label="User Password")
    reg_pwd2 = forms.CharField(widget=forms.PasswordInput(), label="Reenter User Password")
    class Meta:
        model = Registration
        fields = "__all__"
        labels = {
            'reg_name': 'User Name',
            'reg_pwd': 'User Password',
            'reg_pwd2': 'Confirm User Password'
        }


class LoginForm(forms.ModelForm):
    user_pwd = forms.CharField(widget=forms.PasswordInput(), label="User Password")
    class Meta:
        model = User
        fields = "__all__"
        labels = {
            'user_name': 'User Name'
        }


class SearchCityForm(forms.ModelForm):
    class Meta:
        model = RateCity
        fields = ['city']


class RateForm(forms.ModelForm):
    user = forms.CharField(disabled=True),
    city = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea'}), required=True),
    country = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=True),
    nightlife = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True),
    food = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True),
    culture = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True),
    people = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True),
    accommodation = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True),


    class Meta:
        model = RateCity
        fields = ('user', 'city', 'country', 'nightlife', 'food', 'culture', 'people', 'accommodation')