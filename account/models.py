from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, username, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        # user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(primary_key=True)
    activation_code = models.CharField(max_length=20, blank=True)
    username = models.CharField(
        max_length=150,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = [email, username]
    REQUIRED_FIELDS = ['username']
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import random
        activation_code = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f'}
        code = hash(activation_code.get(random.randint(1, 7)))
        self.activation_code = code
        self.save()

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff
