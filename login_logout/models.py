from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, staff=False,
                    active=True, superuser=False):
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.superuser = superuser
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.staff = staff
        user_obj.active = active
        user_obj.last_login = timezone.now()
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password, first_name, last_name):
        return self.create_user(email, password, first_name, last_name, staff=True)

    def create_superuser(self, email, password, first_name, last_name):
        return self.create_user(email, password, first_name, last_name, superuser=True, staff=True)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        return self.active
