from django import forms
from django.forms.widgets import DateInput, Widget
from . models import *
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:  
        # Map the NotesForm to Notes model
        model = Notes 
        # Indicate fields to display
        fields = ['title', 'description']
        

class DateInput(forms.DateInput):
    input_type = 'date' # ELSE the "DUE DATE" will show as a textfield instead of a date field
class HomeworkForm(forms.ModelForm):    
    class Meta:
        # Map the HomeworkForm to Homework model
        model = Homework
        widgets = {'due': DateInput()}
        # Indicate fields to display
        fields = ['subject', 'title', 'description', 'due', 'is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter your search term here:")
    

class TodoForm(forms.ModelForm):
    class Meta:
        # Map the NotesForm to Notes model
        model = Todo
        # Indicate fields to display
        fields = ['title', 'is_finished']


class ConversionForm(forms.Form):
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget = forms.RadioSelect)


class ConversionLengthForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot')]
    input = forms.CharField(
        required=False, label=False, widget=forms.TextInput(
            attrs = {'type': 'number', 'placeholder':'Enter the number'}
        )
    )
    
    measureX = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    
    measureY = forms.CharField(label='', widget=forms.Select(choices=CHOICES))


class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(
        required=False, label=False, widget=forms.TextInput(
            attrs={'type': 'number', 'placeholder': 'Enter the number'}
        )
    )

    measureX = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

    measureY = forms.CharField(label='', widget=forms.Select(choices=CHOICES))


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
