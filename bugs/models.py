from django.db import models
from django.conf import settings


class Bug(models.Model):
    BUG_TYPES = [
        ("error", "Error"),
        ("new_feature", "New Feature"),
        ("improvement", "Improvement"),
        ("test_case", "Test Case")
    ]
    BUG_STATUSES = [
        ("to_do", "To Do"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("under_review", "Under Review"),
        ("done", "Done")
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    bug_type = models.CharField(choices=BUG_TYPES, max_length=20, blank=True, null=True)
    status = models.CharField(choices=BUG_STATUSES, max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Attachment(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="attachments", null=True, blank=True)
    file = models.FileField(
        upload_to='attachments/', null=True, blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Attachment for {self.bug.bug_type} - {self.uploaded_at.strftime('%Y-%m-%d')}"