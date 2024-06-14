from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    qualification = models.CharField(max_length=30, blank=True, null=True)
    department = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.CharField(max_length=60, blank=True, null=True)

    def get_full_name(self) -> str:
        check_name = lambda name : name if name else ''
        return ' '.join([name for name in [self.last_name, self.first_name, self.patronymic] if name])
    
    def get_short_name(self) -> str:
        get_initial = lambda name : name[0] + '.' if name else ''
        return ' '.join([name for name in [self.last_name, get_initial(self.first_name) + get_initial(self.patronymic)] if name])
    class Meta:
        db_table = 'users'
