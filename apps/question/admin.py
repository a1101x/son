from django.contrib import admin

from apps.question.models import Question, Answer, UserAnswer


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_valid', 'is_active']
    list_editable = ['is_valid', 'is_active']
    search_fields = ['question__question_text', 'text']
    list_display_links = ['question', 'text']
    ordering = ['question']
    fieldsets = (
        ('Text', {'fields': ('text',)}),
        ('Question', {'fields': ('question',)}),
        ('Parameters', {'fields': ('is_valid', 'is_active')}),
    )


class QuestionInline(admin.TabularInline):
    model = Answer
    extra = 1

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.answers.all().count() > 0:
            return 0
        return self.extra


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['question_text', 'lesson', 'is_published']
    list_display_links = ['question_text', 'lesson']
    list_editable = ['is_published']
    search_fields = ['question_text', 'lesson__topic', 'lesson__description']
    ordering = ['lesson']
    fieldsets = (
        ('Text', {'fields': ('question_text',)}),
        ('Lesson', {'fields': ('lesson',)}),
        ('Parameters', {'fields': ('is_published',)}),
    )


class UserAnswerAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'question__question_text']
    list_display = ['user', 'question', 'correct', 'answer_time']
    list_display_links = ['user', 'question',]
    readonly_fields = ['correct']
    search_fields = ['user__email', 'question__question_text']
    ordering = ['user', 'question']
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Question', {'fields': ('question',)}),
        ('Parameters', {'fields': ('correct',)}),
    )


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
