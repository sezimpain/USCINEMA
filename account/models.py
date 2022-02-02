from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    email = models.EmailField(primary_key=True)
    activation_code = models.CharField(max_length=20, blank=True)

    EMAIL_FIELD = 'email' # через что логиниться
    REQUIRED_FIELDS = ['first_name'] # обязательные
    USERNAME_FIELD = 'username'

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

