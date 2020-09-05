from django.contrib import admin

from classroom.models import Classroom, Enrollment


class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    list_display = ('student', 'classroom', 'date_joined', 'is_active', 'marks',)
    list_filter = ('date_joined',)
    search_fields = ('classroom__name',)
    readonly_fields = ('student', 'classroom', 'marks',)


class ClassroomAdmin(admin.ModelAdmin):
    model = Classroom
    list_display = ('name', 'section', 'subject', 'room', 'is_active', 'created_at', 'created_by',)
    list_filter = ('is_active', 'created_at',)
    list_editable = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('created_by',)


admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
