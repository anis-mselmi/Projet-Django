from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name',
                  'email', 'department', 'gpa', 'photo']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'First name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Last name'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}),
            'department': forms.Select(
                attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(
                attrs={'class': 'form-control',
                       'step': '0.01'}),
            'photo': forms.FileInput(
                attrs={'class': 'form-control'}),
        }
        labels = {
            'gpa': 'Grade',
        }