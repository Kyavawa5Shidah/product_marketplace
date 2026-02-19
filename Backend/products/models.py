from django.db import models
from django.conf import settings
from accounts.models import Business


class Product(models.Model):

    STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('PENDING', 'Pending Approval'),
    ('APPROVED', 'Approved'),
]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='products'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
