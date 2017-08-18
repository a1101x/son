from django.contrib import admin

from apps.question.models import Question, Answer, UserAnswer


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'is_valid', 'is_active']
    list_editable = ['is_valid', 'is_active']
    search_fields = ['question__question_text', 'text']
    list_display_links = ['id', 'question', 'text']


class QuestionInline(admin.TabularInline):
    model = Answer
    extra = 1
    readonly_fields = ['id']

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.answers.all().count() > 0:
            return 0
        return self.extra


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['question_text', 'is_published']
    list_editable = ['is_published']
    search_fields = ['question_text']


class UserAnswerAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'question__question_text']
    readonly_fields = ['correct']


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
