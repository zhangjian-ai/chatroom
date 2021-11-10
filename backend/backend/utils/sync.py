from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers.errors import BulkIndexError

from db import DBPool


def news_to_es():
    pool = DBPool(
        host="121.4.47.229",
        port=3300,
        user="root",
        password="zm_123456",
        db="chatroom",
        mincached=10
    )
    es = Elasticsearch(hosts=["121.4.47.229:9200"], http_auth=("elastic", "Zj1340026934"))

    # 判断es索引是否存在，不存在就创建
    if not es.indices.exists(index="cars_news"):
        es.indices.create(index="cars_news",
                          mappings={
                              "properties": {
                                  "title": {
                                      "type": "text",
                                      "analyzer": "ik_max_word"
                                  },
                                  "summary": {
                                      "type": "text",
                                      "analyzer": "ik_max_word"
                                  },
                                  "detail_url": {
                                      "type": "text"
                                  },
                                  "img_url": {
                                      "type": "text"
                                  },
                                  "tag": {
                                      "type": "keyword"
                                  }
                              }
                          })

    # 查询临时表，如果有数据就开始同步
    res = pool.query_one(sql="select count(*) count from chatroom.news_temp;")
    if res.get("count"):
        offset = 0
        num = 10

        # 按照每一百条一次来同步
        print("开始同步")
        while offset < res.get("count"):
            sets = pool.query_many(
                sql=f"select id, title, summary, detail_url, img_url, tag from chatroom.news_temp limit {offset}, {num};")

            # 创建actions迭代器
            actions = (
                {
                    "_index": "cars_news",
                    "_op_type": "create",
                    "_id": item.get("id"),
                    "_source": {
                        "title": item.get("title"),
                        "summary": item.get("summary"),
                        "detail_url": item.get("detail_url"),
                        "img_url": item.get("img_url"),
                        "tag": item.get("tag")
                    }
                }
                for item in sets
            )
            try:
                helpers.bulk(es, actions=actions)
            except BulkIndexError:
                pass

            # 增加偏移量
            offset += len(sets)

            print(f"同步进度：{offset} 条！")

        # 删除已同步数据
        pool.execute_one(sql="truncate chatroom.news_temp;")

        print("同步完成")
    else:
        print("暂无同步数据")


if __name__ == '__main__':
    news_to_es()
