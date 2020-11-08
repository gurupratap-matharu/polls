from django.contrib import admin

from classroom.models import Classroom, Enrollment


class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    list_display = ('classroom', 'student', 'date_joined', 'is_active', 'marks',)
    list_filter = ('is_active', 'date_joined',)
    list_editable = ('is_active',)
    search_fields = ('classroom__name',)
    readonly_fields = ('marks',)
    raw_id_fields = ('student', 'classroom',)
    date_hierarchy = 'date_joined'
    ordering = ('is_active', 'classroom', 'student')


class ClassroomAdmin(admin.ModelAdmin):
    model = Classroom
    list_display = ('name', 'section', 'subject', 'room', 'is_active', 'created_at', 'created_by',)
    list_filter = ('is_active', 'created_at',)
    list_editable = ('is_active',)
    search_fields = ('name', 'section', 'subject')
    raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'
    ordering = ('is_active', 'created_at')


admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
