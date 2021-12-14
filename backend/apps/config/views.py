from rest_framework.response import Response
from rest_framework.views import APIView

from backend.utils.configure import ITEMS


class Constance(APIView):
    """系统配置项"""

    def get(self, request):
        """获取常量配置"""
        data = dict()
        for key in ITEMS:
            data.setdefault(key.lower(), [])

            if key.lower() in ("grade",):
                for item in ITEMS[key]:
                    data[key.lower()].append({
                        "id": item[0],
                        "text": item[1]
                    })
            else:
                data[key.lower()] = ITEMS[key]

        return Response(data)
