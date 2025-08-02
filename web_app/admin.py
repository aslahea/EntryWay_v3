from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
    'username', 'email', 'dob', 'bio', 'display_gender', 'marital_status',
    'is_active', 'is_staff', 'is_superuser', 'is_deleted',
    'date_joined', 'delete_action'
    )


    search_fields = (
        'username', 'email', 'dob', 'gender', 'marital_status'
    )

    list_filter = (
        'gender', 'marital_status', 'is_staff', 'is_superuser', 'is_active', 'is_deleted'
    )

    ordering = ('-date_joined',)

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
        'fields': ('dob', 'gender', 'marital_status', 'bio')
        }),

        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Soft Delete Status', {
            'fields': ('is_deleted',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'dob', 'gender', 'marital_status', 'bio',
                'is_active', 'is_staff', 'is_superuser'
            ),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')

    actions = ['soft_delete_selected', 'restore_selected']

    def soft_delete_selected(self, request, queryset):
        count = 0
        for user in queryset:
            if not user.is_deleted:
                user.is_deleted = True
                user.save()
                count += 1
        self.message_user(request, _(
            f"{count} user(s) soft deleted."), messages.SUCCESS)

    soft_delete_selected.short_description = "Soft delete selected users"

    def restore_selected(self, request, queryset):
        count = 0
        for user in queryset:
            if user.is_deleted:
                user.is_deleted = False
                user.save()
                count += 1
        self.message_user(request, _(
            f"{count} user(s) restored."), messages.SUCCESS)

    restore_selected.short_description = "Restore selected users"

    def delete_action(self, obj):
        if not obj.is_deleted:
            return format_html(
                '<span style="color:red;">Use Bulk Action</span>'
            )
        return format_html('<span class="text-muted">Deleted</span>')

    delete_action.short_description = 'Action'

    def get_queryset(self, request):
        """Only show non-deleted users."""
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)

    @admin.display(description='Gender')
    def display_gender(self, obj):
        return obj.get_gender_display()
