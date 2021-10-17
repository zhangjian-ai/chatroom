from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 客户端向服务端发送websocket连接请求时，自动触发。
        # 服务端允许客户端创建连接
        self.accept()

    def websocket_receive(self, message):
        # 客户端基于websocket向服务器发送数据是，自动触发。
        print(message)
        self.send("欢迎大哥光临！")

        # 服务器也可以主动断开连接
        # self.close()

    def websocket_disconnect(self, message):
        # 客户端与服务器断开连接时，自动触发。
        raise StopConsumer
