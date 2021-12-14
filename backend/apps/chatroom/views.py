import json
import random

from django_redis import get_redis_connection
from redis import ResponseError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from file.models import RoomImageModel
from backend.utils import THEME
from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage


class ChatRoomView(APIView):
    """聊天室视图"""

    redis = get_redis_connection("default")

    def get(self, request):
        """
        返回已创建房间信息
        :param request:
        :return:
        """
        try:
            rooms = [json.loads(item.decode()) for item in self.redis.lrange('room', 0, -1)]
        except ResponseError as e:
            return Response({'msg': "拉取房间信息失败", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(rooms, status=status.HTTP_200_OK)

    def post(self, request):
        """
        创建房间。房间信息存入redis
        :param request:
        :return:
        """
        data = request.data

        # 随机生成 4 位 group_id
        group_id = random.randint(0, 9999)
        group_id = str(group_id).zfill(4)

        data['group_id'] = group_id

        # 获取背景图地址
        try:
            image = RoomImageModel.objects.get(theme=(THEME.index(data['theme']) + 1))
            image_url = image.image.__str__()
        except (RoomImageModel.DoesNotExist, ValueError):
            data['img'] = ""
        else:
            client = FastDFSStorage()
            data['img'] = client.url(image_url)

        # 保存房间信息到 redis
        try:
            self.redis.lpush('room', json.dumps(data))
        except ResponseError as e:
            return Response({'msg': "创建房间失败", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(data, status=status.HTTP_201_CREATED)
