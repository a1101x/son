from django.contrib import admin

from apps.question.models import Question, Answer


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_valid', 'is_active']
    list_editable = ['is_valid', 'is_active']
    search_fields = ['question__question_text', 'text']
    list_display_links = ['question', 'text']


class QuestionInline(admin.TabularInline):
    model = Answer
    extra = 1

    def get_extra (self, request, obj=None, **kwargs):
        """
        Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise.
        """
        if obj and obj.answers.all().count() > 0:
            return 0
        return self.extra


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['question_text', 'is_published']
    list_editable = ['is_published']
    search_fields = ['question_text']


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
