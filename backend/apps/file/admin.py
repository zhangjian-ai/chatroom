from django.contrib import admin

from .models import *


@admin.register(RoomImageModel)
class RoomImageAdmin(admin.ModelAdmin):
    # 设置现实字段
    list_display = ['id', 'tag', 'theme', 'image', 'create_time']
