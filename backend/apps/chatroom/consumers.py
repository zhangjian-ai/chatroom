import functools
import json
import time

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from urllib import parse


class ChatConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        # 客户端向服务端发送websocket连接请求时，自动触发。
        # 服务端允许客户端创建连接
        self.accept()

        # 获取url路径参数中的group
        group = self.scope['url_route']['kwargs'].get('group')

        # 获取query传参
        # websocket 握手请求是从 get 升级上来的，所以可以进行query传参
        query_params = {item[0]: item[1] for item in
                        [item.split("=") for item in self.scope['query_string'].decode().split("&")]}
        user_id = query_params['user_id']

        # 将客户端连接对象加入到channel-layer
        # 将异步的channel-layer转成同步方法
        if group:
            # 登陆用户 user_id
            if user_id:
                async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

        # 没有group直接断开
        else:
            raise StopConsumer

    def websocket_receive(self, message):
        # 解析前端json字符串
        data = json.loads(message['text'])

        # 获取url参数中的group
        group = self.scope['url_route']['kwargs'].get('group')

        # 客户端基于websocket向服务器发送数据时，自动触发本方法。
        if group:
            # 准备返回数据，加上系统时间
            t = time.strftime("%H:%M:%S", time.localtime())
            data['time'] = t
            async_to_sync(self.channel_layer.group_send)(group, {"type": "call", "msg": json.dumps(data)})

    def call(self, event):
        """回调函数，实现向客户端发送消息"""
        text = event['msg']
        self.send(text)

    def websocket_disconnect(self, message):
        # 获取url参数中的group
        group = self.scope['url_route']['kwargs'].get('group')

        # 某个客户端断开连接时，将其从group中删除
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)

        # 客户端与服务器断开连接时，自动触发。
        raise StopConsumer
