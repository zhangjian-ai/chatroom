from elasticsearch import ElasticsearchException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings


class EsNewsSearch(APIView):
    """
    ES查询接口
    """

    def get(self, request):
        # 获取查询文本
        content = request.query_params.get("content")
        tag = request.query_params.get("tag")
        page = int(request.query_params.get("page"))
        size = int(request.query_params.get("size"))

        # ES查询语句
        query = {"bool": {"must": []}}

        # 组装查询条件
        if content:
            query["bool"]["must"].append({"multi_match": {"query": content, "fields": ["title", "summary"]}})
        if tag:
            query["bool"]["must"].append({"match_phrase": {"tag": {"query": tag}}})

        # 默认查询
        if len(query["bool"]["must"]) == 0:
            query["bool"]["must"].append({"match_all": {}})

        # 高亮查询关键字
        highlight = {
            "pre_tags": "<font style='color:red;'>",
            "post_tags": "</font>",
            "require_field_match": "false",
            "fields": {
                "*": {}
            }
        }

        # 查询
        try:
            result = settings.ES.search(index="cars_news",
                                        query=query,
                                        highlight=highlight,
                                        from_=(page-1) * size,
                                        size=size,
                                        filter_path=["hits.hits", "hits.total"])
        except ElasticsearchException as e:
            return Response({'msg': 'ES查询异常', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=result)
