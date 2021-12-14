from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from backend.utils import THEME, BaseModel
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage


class RoomImageModel(BaseModel):
    """
    聊天室主题图片
    """

    image = models.ImageField(verbose_name="图片地址")
    theme = models.SmallIntegerField(choices=[(index, item) for index, item in enumerate(THEME)], unique=True,
                                     verbose_name="主题")
    tag = models.CharField(max_length=20, default="room")

    class Meta:
        db_table = "room_theme"
        verbose_name = "聊天室主题图片"
        verbose_name_plural = verbose_name


# 信号监听
@receiver(post_delete, sender=RoomImageModel)
def delete_storage(sender, **kwargs):
    storage = FastDFSStorage()
    storage.delete(kwargs['instance'].image.__str__())
