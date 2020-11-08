from django.contrib import admin

from polls.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = (ChoiceInline,)
    list_display = ('question_text', 'slug', 'pub_date', 'created_by')
    list_filter = ('pub_date',)
    prepopulated_fields = {"slug": ("question_text",)}
    search_fields = ('question_text',)
    raw_id_fields = ('created_by',)
    date_hierarchy = 'pub_date'
    ordering = ('pub_date', 'created_by',)


admin.site.register(Question, QuestionAdmin)
