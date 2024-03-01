from django.contrib import admin
from .models import Bug, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1  # Number of extra empty forms


class BugAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline, ]


admin.site.register(Bug, BugAdmin)

