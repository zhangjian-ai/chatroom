from django.contrib.auth.models import AbstractUser
from django.db import models

from backend.utils import GRADE


class User(AbstractUser):
    mobile = models.BigIntegerField(verbose_name="手机号", unique=True)
    nickname = models.CharField(max_length=50, verbose_name="姓名")
    grade = models.SmallIntegerField(choices=GRADE, verbose_name="职级")

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname
