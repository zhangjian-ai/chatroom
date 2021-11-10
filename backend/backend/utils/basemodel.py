from django.db import models
from django.utils import timezone


class CustomDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        """重写该方法，在保存之前完成时间格式化"""
        val = super().pre_save(model_instance, add)
        val = timezone.datetime.strftime(val, '%Y-%m-%d %H:%M:%S')

        return val


class BaseModel(models.Model):
    """模型基类"""

    create_time = CustomDateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = CustomDateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True
