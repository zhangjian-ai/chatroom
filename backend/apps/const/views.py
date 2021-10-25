from rest_framework.response import Response
from rest_framework.views import APIView

from backend.libs.configure import *


class Constance(APIView):
    """系统配置项"""

    def get(self, request):
        """获取常量配置"""
        data = dict()
        grade = list()
        for item in GRADE:
            grade.append({
                "id": item[0],
                "text": item[1]
            })

        data['grade'] = grade

        return Response(data)
