import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from auditlog.models import AuditlogHistoryField



class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    changelog = AuditlogHistoryField()

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["first_name", "username"]

    def __str__(self):
        return self.first_name if self.first_name else self.username
