from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LogonSerializer
from .models import User
from backend.utils.jwt import create_jwt_token


class LogonView(CreateAPIView):
    """注册视图"""
    permission_classes = []

    serializer_class = LogonSerializer


class LoginView(APIView):
    """登录视图"""
    permission_classes = []

    def post(self, request):
        username = request.data.pop("username")
        password = request.data.pop("password")

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({'msg': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
            # 密码校验成功则返回登陆信息
            token = create_jwt_token(user)
            return Response({'id': user.id, 'nickname': user.nickname, 'token': token})
        except User.DoesNotExist:
            return Response({'msg': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
