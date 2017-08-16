from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from apps.userprofile.forms import UserChangeForm, UserCreationForm
from apps.userprofile.models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'is_admin', 'is_blocked', 'send_app', 'block_user')
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff')}),
        ('Blocked', {'fields': ('is_blocked',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def send_app(self, obj):
        return format_html(
            '<a class="button" href="{}">Android</a>&nbsp;&nbsp;'
            '<a class="button" href="{}">iOS</a>',
            reverse('userprofile:send_android', args=[obj.email]),
            reverse('userprofile:send_ios', args=[obj.email]),
        )

    send_app.short_description = 'Send App'
    send_app.allow_tags = True

    def block_user(self, obj):
        if not obj.is_admin:
            if obj.is_blocked:
                return format_html(
                    '<a class="button" href="{}" style="color:red">Unblock User</a>',
                    reverse('userprofile:block_user', args=[obj.email]),
                )
            else:
                return format_html(
                    '<a class="button" href="{}">Block User</a>',
                    reverse('userprofile:block_user', args=[obj.email]),
                )

    block_user.short_description = 'Block User'
    block_user.allow_tags = True


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
