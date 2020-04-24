from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

from django.core.validators import RegexValidator

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('F', 'Nữ'),
        ('M', 'Nam'),
    )
    PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'.")

    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(validators=[PHONE_REGEX], max_length=17, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    fullname = models.CharField(max_length=256)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_joined = models.DateTimeField(default=timezone.now)
    blocked_date = models.DateTimeField(blank=True, null=True, default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    class Meta:
        db_table = 'user'