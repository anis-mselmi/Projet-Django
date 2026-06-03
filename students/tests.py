from django.test import TestCase

from .forms import StudentForm
from .models import Department


class StudentFormTests(TestCase):
    def _valid_form_data(self, **overrides):
        data = {
            'first_name': 'Test',
            'last_name': 'Student',
            'email': 'test.student@example.com',
            'gpa': '3.5',
            'department': 'Informatique',
        }
        data.update(overrides)
        return data

    def test_department_reuses_existing_case_insensitive_name(self):
        department = Department.objects.create(name='Informatique')

        form = StudentForm(data=self._valid_form_data(department='  informatique  '))

        self.assertTrue(form.is_valid(), form.errors)
        student = form.save()
        self.assertEqual(student.department_id, department.id)
        self.assertEqual(Department.objects.count(), 1)

    def test_department_created_with_title_case_when_missing(self):
        form = StudentForm(data=self._valid_form_data(department='  genie logiciel  '))

        self.assertTrue(form.is_valid(), form.errors)
        student = form.save()
        self.assertEqual(student.department.name, 'Genie Logiciel')

    def test_gpa_validation_rejects_out_of_range_values(self):
        low_form = StudentForm(data=self._valid_form_data(gpa='-1'))
        high_form = StudentForm(
            data=self._valid_form_data(email='high@example.com', gpa='5')
        )

        self.assertFalse(low_form.is_valid())
        self.assertIn('gpa', low_form.errors)
        self.assertFalse(high_form.is_valid())
        self.assertIn('gpa', high_form.errors)

    def test_gpa_validation_rejects_non_numeric_values(self):
        form = StudentForm(data=self._valid_form_data(gpa='not-a-number'))

        self.assertFalse(form.is_valid())
        self.assertIn('gpa', form.errors)
