from django.contrib import admin

from .models import Choice, Question, Quiz


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class QuestionInline(admin.TabularInline):
    model = Question


class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title_text']}),
        ('Quiz description', {'fields': ['quiz_text']}),
    ]
    inlines = [QuestionInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
