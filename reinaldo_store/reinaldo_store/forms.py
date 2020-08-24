from django import forms

#from django.contrib.auth.models import User
from users.models import User

class RegisterForm(forms.Form):
    #Clase con la que se obtienen los datos de cada usuario.
    username = forms.CharField(required=True, min_length=4, 
                                max_length=50, 
                                widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email',
                                                                          'placeholder': 'Example@gmail.com'}))
    password = forms.CharField(required=True, min_length=6, max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password',
                                                                                                         'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        #Función para no permitir usuarios repetidos.
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('The user is already in use')

        return username

    def clean_email(self):
        #Función para no permitir emails repetidos.
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email is already in use')

        return email

    def clean(self):
        #Función para verificar la contraseña.
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'The password does not match')

    def save(self):
        #Función para guardar los datos ingresados por el usuario.
        return User.objects.create_user(
                self.cleaned_data.get('username'),
                self.cleaned_data.get('email'),
                self.cleaned_data.get('password'),
            )