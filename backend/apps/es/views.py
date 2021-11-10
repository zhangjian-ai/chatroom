from rest_framework.views import APIView
from django.conf import settings

class EsSearch(APIView):
    """
    ES查询接口
    """

    def get(self, request):
        # 获取查询文本
        content = request.query_params.get("content")

