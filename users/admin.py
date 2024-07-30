from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from users.models import Territory, Language, WikimediaProject, CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class AccountUserAdmin(AuthUserAdmin):
    list_display = ('username', 'is_staff', 'is_active')

    fieldsets = (
        (None, {
            "fields": (
                'username', 'password'
            ),
        }),
        ('Personal info', {
            'fields': (
                'email',
            ),
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
        ('Important dates', {
            'fields': (
                'last_login', 'date_joined'
            ),
        }),        
    )
    
    
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(AccountUserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [ProfileInline]
        return super(AccountUserAdmin, self).change_view(*args, **kwargs)


admin.site.register(CustomUser, AccountUserAdmin)
admin.site.register(Territory)
admin.site.register(Language)
admin.site.register(WikimediaProject)
admin.site.register(Profile)
