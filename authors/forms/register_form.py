from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

        # add_attr(self.fields['username'], 'css', 'a-css-class')

    username = forms.CharField(
        error_messages={'required': 'This field must not be empty'},
        min_length=4,
        max_length=150,
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'This field must not be empty',
        },
        help_text=(
            'Password must have at leat one uppercase letter, '
            'one lowercase letter and one number. THe length should be'
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'

    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, repeat your password',
        },
    )

    email = forms.EmailField(
        error_messages={
            'required': 'E-mail is required',
        },
        label='E-mail',
        help_text=('The e-mail must be valid.'),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
        }

    # def clean_password(self):
    #    data = self.cleaned_data.get('password')
    #    if 'atenção' in data:
    #        raise ValidationError(
    #            'Não digite %(value)s no campo password',
    #            code='invalid',
    #            params={'value': 'atenção'}
    #        )
    #
    #
    #    return data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('User e-mail is alreade in use',
                                  code='invalid',
                                  )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            }
            )
