from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from users.models import Region, Language, WikimediaProject, AreaOfInterest, Organization, CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class AccountUserAdmin(AuthUserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(AccountUserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [ProfileInline]
        return super(AccountUserAdmin, self).change_view(*args, **kwargs)


admin.site.register(CustomUser, AccountUserAdmin)
admin.site.register(Organization)
admin.site.register(Region)
admin.site.register(Language)
admin.site.register(WikimediaProject)
admin.site.register(AreaOfInterest)
admin.site.register(Profile)
