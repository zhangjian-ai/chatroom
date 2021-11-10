import re

from rest_framework import serializers

from .models import User
from backend.utils.token import create_jwt_token


class LogonSerializer(serializers.ModelSerializer):

    confirm = serializers.CharField(label="确认密码", write_only=True)
    token = serializers.CharField(label="TOKEN", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'password', 'confirm', 'mobile', 'grade', 'token']

        extra_kwargs = {
            'username': {
                'write_only': True
            },
            'password': {
                'write_only': True
            },
            'mobile': {
                'write_only': True
            },
            'grade': {
                'write_only': True
            },
        }

    def validate(self, attrs):
        # 验证手机号
        mobile = attrs.get('mobile')

        if not re.match('^1[3-9]\d{9}$', str(mobile)):
            raise serializers.ValidationError('手机号不合法')

        # 验证两次输入的密码是否一致
        if attrs.get('password') != attrs.pop('confirm'):
            raise serializers.ValidationError('两次输入密码不一致')

        return attrs

    def create(self, validated_data):
        # 创建新对象
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # 此时还缺少序列化字段token
        token = create_jwt_token(user)

        user.token = token

        return user
