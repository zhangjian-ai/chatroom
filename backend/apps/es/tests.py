from elasticsearch import Elasticsearch
from elasticsearch import helpers

# 创建 es 连接客户端
es = Elasticsearch(hosts=["121.4.47.229:9200"], http_auth=("elastic", "Zj1340026934"))

# 创建索引

# body = {
#     "name": "小强",
#     "age": 20
# }

# result_1 = es.create(index="py_demo1", id="4", document={"name": "阿强", "age": 18})

# result_1 = es.index(index="py_demo1", id="5", op_type="create", document={"name": "博强", "age": 18})

# result_1 = es.get(index="py_demo1", id="2")

# result_1 = es.search(index="py_demo1", query={"match": {"name": "强"}})

# result_1 = es.search(index="py_demo1", query={"bool": {"must": {"match_phrase": {"name": "阿强"}}}})

# result_1 = es.search(index="py_demo1", query={"range": {"age": {"gt": 18}}}, filter_path="hits.hits._source")

# result_1 = es.search(index="py_demo1", query={"match_all": {}}, filter_path="hits.hits",
#                      _source_includes=["name"])

# result_1 = es.delete_by_query(index="py_demo1", body={"query": {"ids": {"values": ["2", "3"]}}})

# result_1 = es.index(index="py_demo1", id="2", document={"name": "李寻欢", "age": 26})

# result_1 = es.update(index="py_demo1", id="2", body={"doc": {"name": "张小强"}})


# query = {
#     "match": {
#         "title": "SUV"
#     }
# }
#
# result_1 = es.search(index="cars_news", query=query, filter_path="hits.hits", size=100)
#
# print(result_1)

# print(es.cat.indices(format='json'))

# response = es.indices.create(index="py_demo3",
#                              mappings={"properties": {"name": {"type": "text"}, "age": {"type": "short"}}},
#                              settings={"number_of_shards": 1, "number_of_replicas": 2})
# print(response)


# print(es.indices.get_mapping(index="py_demo3"))
# print(es.indices.get_alias(index="py_demo3"))
# print(es.indices.get_settings(index="py_demo3"))
# print(es.indices.put_alias(index="py_demo3", name="py3"))
# print(es.cat.nodes())
# print(es.cat.master())
# print(es.cat.health())

# body = [
#     {"create": {"_id": 8}},
#     {"name": "西门吹雪", "age": 22},
#     {"update": {"_id": 5}},
#     {"doc": {"name": "伯强"}}
# ]
# print(es.bulk(index="py_demo1", body=body))

# actions = [
#     {
#         "_index": "py_demo1",
#         "_op_type": "create",
#         "_id": "9",
#         "_source": {
#             "name": "花满楼",
#             "age": 20
#         }
#     },
#     {
#         "_index": "py_demo1",
#         "_op_type": "create",
#         "_id": "10",
#         "_source": {
#             "name": "陆小凤",
#             "age": 22
#         }
#     },
#     {
#         "_index": "py_demo1",
#         "_op_type": "update",
#         "_id": "5",
#         "_source": {
#             "doc": {
#                 "name": "江流儿",
#                 "age": 14
#             }
#         }
#     },
#     {
#         "_index": "py_demo1",
#         "_op_type": "delete",
#         "_id": "4"
#     }
# ]
#
# s = helpers.bulk(es, actions=actions)
#
# print(s)
#
# print(es.indices.exists(index="cars_news"))
#
# print(es.indices.delete(index="cars_news"))

# print(es.search(index="cars_news", query={"match_phrase": {"title": "SUV"}}, filter_path="hits", from_=20, size=100))

# suggest = {
#     "my_suggest": {
#         "text": "new",
#         "term": {
#             "field": "tag"
#         }
#     }
# }
#
# query = {
#     "match": {
#         "title": "宝马"
#     }
# }
#
# print(es.search(index="cars_news", suggest=suggest, query=query, filter_path=["suggest"]))

suggest = {
    "news_suggest": {
        "prefix": "宝马",
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

print(es.search(index="cars_news", suggest=suggest, filter_path=["suggest.news_suggest"]))
