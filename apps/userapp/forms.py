from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class RegisterForm(UserCreationForm):
    userChoice = (
        ('CUS', 'Customer'),
        ('VEN', 'Vendor'),
        ('WHO', 'Wholesaler'),
        # ('DEL', 'Delivery'),
        # ('OTH', 'Other'),
    )

    role = forms.ChoiceField(choices=userChoice, required=False)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    place = forms.CharField(max_length=255)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-dark'))