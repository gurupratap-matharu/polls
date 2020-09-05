from django.contrib import admin

from polls.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline,)
    list_display = ('question_text', 'pub_date', 'created_by')
    list_filter = ('pub_date',)
    search_fields = ('question_text',)
    model = Question
    readonly_fields = ('created_by',)


admin.site.register(Question, QuestionAdmin)
