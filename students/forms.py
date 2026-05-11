from django import forms
from .models import Student, Department

class StudentForm(forms.ModelForm):
    # Free-text field — user types any department name
    department = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. Informatique, Mathématiques…'}),
        label='Department',
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name',
                  'email', 'gpa', 'photo']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'First name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Last name'}),
            'email': forms.EmailInput(
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill the text field with the current department name when editing
        if self.instance and self.instance.pk and self.instance.department:
            self.fields['department'].initial = self.instance.department.name

    def save(self, commit=True):
        student = super().save(commit=False)

        # Handle department free-text input
        dept_name = self.cleaned_data.get('department', '').strip()
        if dept_name:
            dept, _ = Department.objects.get_or_create(name=dept_name)
            student.department = dept
        else:
            student.department = None

        # Explicitly assign the photo so the file is written to disk on save()
        photo = self.cleaned_data.get('photo')
        if photo and hasattr(photo, 'name'):
            # A new file was uploaded
            student.photo = photo
        elif not self.files.get('photo') and self.instance.pk:
            # No new file — keep the existing photo (editing mode)
            student.photo = self.instance.__class__.objects.get(pk=self.instance.pk).photo

        if commit:
            student.save()
        return student