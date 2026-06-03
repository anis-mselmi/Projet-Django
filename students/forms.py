from django import forms
from django.core.exceptions import ValidationError
from .models import Student, Department


class StudentForm(forms.ModelForm):
    """Form for creating and editing Student records.
    
    This form provides a user-friendly interface for managing student information,
    including validation for GPA and automatic department creation/lookup.
    """
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
                       'step': '0.01',
                       'min': '0.0',
                       'max': '4.0'}),
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

    def clean_gpa(self):
        """Validate GPA is between 0.0 and 4.0 inclusive."""
        gpa = self.cleaned_data.get('gpa')
        if gpa is None:
            return gpa
        try:
            gpa_val = float(gpa)
        except (TypeError, ValueError):
            raise ValidationError('Enter a valid number for GPA.')
        if gpa_val < 0.0 or gpa_val > 4.0:
            raise ValidationError('GPA must be between 0.0 and 4.0.')
        return gpa_val

    def clean_email(self):
        """Validate email uniqueness for new students."""
        email = self.cleaned_data.get('email')
        if email and self.instance.pk is None:
            # Only check uniqueness for new students (not during edit)
            if Student.objects.filter(email=email).exists():
                raise ValidationError('A student with this email already exists.')
        return email

    def save(self, commit=True):
        """Save the student with automatic department handling.
        
        If a department name is provided, it will either find an existing
        department with that name (case-insensitive) or create a new one.
        """
        student = super().save(commit=False)

        # Handle department free-text input: normalize and do case-insensitive lookup
        dept_name_raw = self.cleaned_data.get('department', '')
        dept_name = dept_name_raw.strip()
        if dept_name:
            dept = Department.objects.filter(name__iexact=dept_name).first()
            if not dept:
                dept = Department.objects.create(name=dept_name.title())
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
