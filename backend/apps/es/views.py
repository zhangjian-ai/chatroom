from elasticsearch import ElasticsearchException, Elasticsearch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

ES = Elasticsearch(hosts=["121.4.47.229:9200"], http_auth=("elastic", "Zj1340026934"))


class EsNewsSearchView(APIView):
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
            # tag字段是keyword类型，使用term查询效率更高
            query["bool"]["must"].append({"term": {"tag": {"value": tag}}})

        # 默认查询
        if len(query["bool"]["must"]) == 0:
            query["bool"]["must"].append({"match_all": {}})

        # 高亮查询关键字
        highlight = {
            "pre_tags": "<font style='color:red;'>",
            "post_tags": "</font>",
            "require_field_match": "true",
            "fields": {
                "*": {}
            }
        }

        # 查询
        try:
            result = ES.search(index="cars_news",
                               query=query,
                               highlight=highlight,
                               from_=(page - 1) * size,
                               size=size,
                               filter_path=["hits.hits", "hits.total"],
                               track_total_hits=True)
        except ElasticsearchException as e:
            return Response({'msg': 'ES查询异常', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=result)


class EsNewsSuggestView(APIView):
    """
    ES建议信息接口
    """

    def get(self, request):
        # 获取查询文本
        content = request.query_params.get("content")

        if not content:
            return Response(data={"suggest": []})

        # ES建议语句
        suggest = {
            "news_suggest": {
                "prefix": content,
                "completion": {
                    "field": "title.suggest",
                    "skip_duplicates": True,
                    "fuzzy": {
                        "fuzziness": 2,
                        "min_length": 3,
                        "prefix_length": 2
                    }
                }
            }
        }

        # 查询
        try:
            result = ES.search(index="cars_news",
                               suggest=suggest,
                               size=5,
                               filter_path=["suggest.news_suggest"])
        except ElasticsearchException as e:
            return Response({'msg': 'ES查询异常', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = [item.get("text") for item in result['suggest']['news_suggest'][0]["options"]]
        return Response(data={"suggest": data})
