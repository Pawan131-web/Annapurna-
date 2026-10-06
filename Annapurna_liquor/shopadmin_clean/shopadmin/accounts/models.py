from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extends the built-in User with a role, so employees can be added later."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.ADMIN)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_username()} ({self.get_role_display()})'

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN
