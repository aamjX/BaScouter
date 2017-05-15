from django.contrib.auth.models import User
from django import forms
from apps.usuario.models import Profile, SearchValues, Comment
from django.contrib.auth.forms import UserCreationForm

'''----------------------------------------------------------------------------------------------------------'''

'''Formulario de autenticacion'''

'''----------------------------------------------------------------------------------------------------------'''

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
                               max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
                               max_length=100, required=True)

'''----------------------------------------------------------------------------------------------------------'''

'''Formulario de registro de un usuario'''

'''----------------------------------------------------------------------------------------------------------'''

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre de usuario'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellidos'}),
        }

'''----------------------------------------------------------------------------------------------------------'''

'''Formularios relacionados con la actualizacion de datos de un usuario'''

'''----------------------------------------------------------------------------------------------------------'''

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sex','bio', 'location', 'birth_date', 'image',)
        labels = {
            'sex': 'Sexo',
            'bio': 'Biografía',
            'location':'Localización',
            'birth_date':'Fecha de nacimiento',
            'image':'Imágen de perfil',
        }
        widgets = {
            'sex': forms.Select(attrs={'class':'form-control'}, choices=(('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Otro', 'Otro'))),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control',}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),

        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name':'Apellidos',
            'email':'Correo electrónico',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
        }

'''----------------------------------------------------------------------------------------------------------'''

'''Formulario simple para comentar en el perfil de un usuario'''

'''----------------------------------------------------------------------------------------------------------'''

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribir...'}),
        }

'''----------------------------------------------------------------------------------------------------------'''

'''Formulario para la busqueda avanzada de jugadores'''

'''----------------------------------------------------------------------------------------------------------'''

class SearchValuesForm(forms.ModelForm):
    class Meta:
        model = SearchValues
        fields = ('squad','principals', 'yellowCards', 'redCards', 'goalkeeper_goals',
                  'goalkeeper_assists', 'goalkeeper_ownGoals', 'defence_goals', 'defence_assists', 'defence_ownGoals',
                  'midfield_goals', 'midfield_assists', 'midfield_ownGoals', 'striker_goals',
                  'striker_assists', 'striker_ownGoals')
        labels = {
            'squad': 'Puntuación por partidos convocados',
            'principals': 'Puntuación por partidos como titular',
            'yellowCards':'Tarjetas amarillas',
            'redCards':'Tarjetas rojas',
            'goalkeeper_goals':'Goles',
            'goalkeeper_assists': 'Pases de gol',
            'goalkeeper_ownGoals':'Goles en propia meta',
            'defence_goals':'Goles',
            'defence_assists':'Pases de gol',
            'defence_ownGoals':'Goles en propia meta',
            'midfield_goals':'Goles',
            'midfield_assists':'Pases de gol',
            'midfield_ownGoals':'Goles en propia meta',
            'striker_goals':'Goles',
            'striker_assists': 'Pases de gol',
            'striker_ownGoals': 'Goles en propia meta',
        }
        widgets = {
            'squad': forms.NumberInput(attrs={'class': 'form-control', 'max':'10.0', 'min':'-10.0', 'step':'0.1'}),
            'principals': forms.NumberInput(attrs={'class': 'form-control', 'max':'10', 'min':'-10', 'step':'0.1'}),
            'yellowCards': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'redCards': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'goalkeeper_goals': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'goalkeeper_assists': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'goalkeeper_ownGoals': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'defence_goals': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'defence_assists': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'defence_ownGoals': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'midfield_goals': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'midfield_assists': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'midfield_ownGoals': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'striker_goals': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'striker_assists': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
            'striker_ownGoals': forms.NumberInput(attrs={'class': 'form-control', 'max': '10', 'min': '-10', 'step':'0.1'}),
        }