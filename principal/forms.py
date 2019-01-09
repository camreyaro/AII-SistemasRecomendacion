from django import forms

class UsuarioForm(forms.Form):
    usuario = forms.CharField(label='Usuario', max_length=100)
        
class PeliculaForm(forms.Form):
    pelicula = forms.CharField(label='Pelicula', max_length=100)