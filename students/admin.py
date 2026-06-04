from django.contrib import admin
from .models import Student, Department


class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for Department model.
    
    Provides a user-friendly admin panel for managing departments
    with their names and descriptions.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)


class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student model.
    
    Provides a comprehensive admin panel for managing students,
    including display of key fields, filtering, and search capabilities.
    """
    list_display = ('first_name', 'last_name', 'email', 'department', 'gpa', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at',)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Student, StudentAdmin)
