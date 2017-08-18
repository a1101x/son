from django.contrib import admin

from apps.lesson.models import LessonSet, Lesson, Page, Favorite, LogLesson


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
    ordering = ['id']
    fieldsets = (
        ('Text', {'fields': ('topic', 'description')}),
        ('Files', {'fields': ('image', 'file')}),
        ('ImageInfo', {'fields': ('height_field', 'width_field')}),
    )


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
    ordering = ['lesson_set']
    fieldsets = (
        ('Text', {'fields': ('topic', 'description')}),
        ('LessonSet', {'fields': ('lesson_set',)}),
        ('Files', {'fields': ('image', 'file')}),
        ('ImageInfo', {'fields': ('height_field', 'width_field')}),
    )


class PageAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'page_number', 'text']
    search_fields = ['lesson__topic', 'lesson__description', 'text', 'page_number']
    list_display_links = ['lesson', 'page_number']
    ordering = ['lesson', 'page_number']
    fieldsets = (
        ('Text', {'fields': ('text',)}),
        ('PageNumber', {'fields': ('page_number',)}),
        ('Lesson', {'fields': ('lesson',)}),
        ('Files', {'fields': ('image', 'file')}),
        ('ImageInfo', {'fields': ('height_field', 'width_field')}),
    )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'page']
    search_fields = ['user__email', 'page__text', 'page__page_number']
    ordering = ['user', 'page']
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Page', {'fields': ('page',)}),
    )


class LogLessonAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_viewed']
    search_fields = ['user__email', 'lesson__topic', 'lesson__description']
    ordering = ['user', 'lesson']
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Lesson', {'fields': ('lesson',)}),
        ('Parameters', {'fields': ('is_viewed',)}),
    )


admin.site.register(LessonSet, LessonSetAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(LogLesson, LogLessonAdmin)
