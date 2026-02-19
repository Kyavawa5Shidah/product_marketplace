from django.db import models
from django.contrib.auth.models import AbstractUser


class Business(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('EDITOR', 'Editor'),
        ('APPROVER', 'Approver'),
        ('VIEWER', 'Viewer'),
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    can_create_product = models.BooleanField(default=False)
    can_edit_product = models.BooleanField(default=False)
    can_delete_product = models.BooleanField(default=False)
    can_approve_product = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'business')


class User(AbstractUser):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
