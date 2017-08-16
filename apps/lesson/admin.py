from django.contrib import admin

from apps.lesson.models import LessonSet, Lesson, Page


class LessonSetInline(admin.TabularInline):
    model = Lesson
    extra = 1

    def get_extra (self, request, obj=None, **kwargs):
        """
        Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise.
        """
        if obj and obj.lessons.all().count() > 0:
            return 0
        return self.extra


class LessonSetAdmin(admin.ModelAdmin):
    inlines = [LessonSetInline]
    list_display = ['topic', 'description']
    search_fields = ['topic', 'description']


class LessonInline(admin.TabularInline):
    model = Page
    extra = 1

    def get_extra (self, request, obj=None, **kwargs):
        """
        Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise.
        """
        if obj and obj.pages.all().count() > 0:
            return 0
        return self.extra


class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['topic', 'description']
    search_fields = ['topic', 'description', 'lesson_set__topic', 'lesson_set__description']


class PageAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'page_number', 'text']
    search_fields = ['lesson__topic', 'lesson__description', 'text', 'page_number']
    list_display_links = ['lesson', 'page_number']


admin.site.register(LessonSet, LessonSetAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Page, PageAdmin)
