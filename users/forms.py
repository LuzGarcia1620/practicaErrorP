from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel','password1', 'password2']
        
        widgets={
            'email':forms.EmailInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'correo electronico',
                    'required': True,
                    'minlength': '22',
                    'maxlength':'22',
                    'pattern': '^[0-9]{5}tn[0-9]{3}@utez\.edu\.mx$',
                    'title':'Ingrese un correo institucional válido'
                } 
            ),
             'name':forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'name',
                    'required': True,
                    'minlength': '1',
                    'maxlength':'150',
                    'pattern': '^[a-zA-Z]+$',
                    'title':'Ingrese un nombre válido',
                } 
            ),
            'surname':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'surname',
                    'required': True,
                    'minlength': '2',
                    'maxlength':'50',
                    'pattern': '^[a-zA-Z]+$',
                    'title':'Ingrese un apellido válido'
                }
            ),
            'control_number':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese numero de control',
                    'required': True,
                    'minlength': '10',
                    'maxlength':'10',
                    'pattern': '^[0-9]{5}tn[0-9]{3}$',
                    'title':'Ingrese su matricula de la UTEZ'
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su edad',
                    'required': True,
                    'min': '1',  
                    'max': '2',
                    'pattern': '^[0-9]{1,2}$',  
                    'title': 'Ingrese su edad'
                }
            ),

            'tel':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su telefono',
                    'required': True,
                    'minlength': '10',
                    'maxlength':'10',
                    'pattern':'^[0-9]{10}$',
                    'title':'Ingrese un telefono válido'
                }
            ),
            'password1':forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su contraseña',
                    'required': True,
                    'minlength': '8',
                    'maxlength':'50',
                    'pattern':'^(?=.*[0-9])(?=.*[!#$%&?]).{8,}$',
                    'title':'La contraseña debe tener al menos 8 caracteres, incluir un número y al menos un símbolo'
                }
            ),
            'password2':forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'confirme su contraseña',
                    'required': True,
                    'minlength': '8',
                    'maxlength':'50',
                    'pattern':'^(?=.*[0-9])(?=.*[!#$%&?])(?=.*[A-Z]).{8,}$',
                    'title':'Ingrese nuevamente la contraseña'
                }
            ),
        }

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if not re.match(r'^[0-9]{5}tn[0-9]{3}@utez\.edu\.mx$', email):
                raise forms.ValidationError("El correo electrónico debe ser institucional y tener el formato: [matricula]@utez.edu.mx")
            return email

        def clean_control_number(self):
            control_number = self.cleaned_data.get('control_number')
            if len(control_number) != 10 or not re.match(r'^[0-9]{5}tn[0-9]{3}$', control_number):
                raise forms.ValidationError("La matrícula debe tener exactamente 10 caracteres con el formato: [00000tn000]")
            return control_number

        def clean_tel(self):
            tel = self.cleaned_data.get('tel')
            if len(tel) != 10 or not re.match(r'^[0-9]{10}$', tel):
                raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos.")
            return tel

        def clean_password1(self):
            password1 = self.cleaned_data.get('password1')
            if not re.match(r'^(?=.\d)(?=.[A-Z])(?=.*[!#$%&?])[A-Za-z\d!#$%&?]{8,}$', password1):
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres, 1 número, 1 letra mayúscula y 1 símbolo (como !, #, $, %, & o ?).")
            return password1

        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')

            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            
            return cleaned_data
        

class CustomUserLoginForm(AuthenticationForm):
    email = forms.CharField(label="Correo electrónico", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return cleaned_data
    