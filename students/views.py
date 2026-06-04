from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm


def student_list(request):
    """Display a paginated list of students with search functionality.
    
    Query Parameters:
        q (str): Optional search query to filter students by first or last name
        page (int): Page number for pagination (default: 1)
    
    Context:
        students: Paginated student queryset
        query: The search query string
    """
    query = request.GET.get('q', '')
    students = Student.objects.filter(
        first_name__icontains=query
    ) | Student.objects.filter(
        last_name__icontains=query
    ) if query else Student.objects.all()
    paginator = Paginator(students, 5)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    return render(request, 'students/list.html',
                  {'students': students, 'query': query})


@login_required
def student_create(request):
    """Create a new student record.
    
    Requires user to be logged in.
    
    Methods:
        GET: Display the student creation form
        POST: Create a new student and redirect to student list
    
    Returns:
        Redirect to student_list on success
        Render form template with errors on validation failure
    """
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/form.html',
                  {'form': form, 'title': 'Add Student'})


@login_required
def student_update(request, pk):
    """Update an existing student record.
    
    Requires user to be logged in.
    
    Args:
        pk (int): Primary key of the student to update
    
    Methods:
        GET: Display the student edit form
        POST: Update the student and redirect to student list
    
    Returns:
        Redirect to student_list on success
        Render form template with errors on validation failure
        404 response if student not found
    """
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/form.html',
                  {'form': form, 'title': 'Edit Student'})


@login_required
def student_delete(request, pk):
    """Delete a student record.
    
    Requires user to be logged in.
    
    Args:
        pk (int): Primary key of the student to delete
    
    Methods:
        GET: Display delete confirmation page
        POST: Delete the student and redirect to student list
    
    Returns:
        Redirect to student_list on successful deletion
        Render confirmation template to confirm deletion
        404 response if student not found
    """
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html',
                  {'student': student})