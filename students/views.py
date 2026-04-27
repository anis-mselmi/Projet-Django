from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm

def student_list(request):
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
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/form.html',
                  {'form': form, 'title': 'Add Student'})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/form.html',
                  {'form': form, 'title': 'Edit Student'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html',
                  {'student': student})