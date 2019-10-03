from flask_restful import reqparse
from flask_restful import Resource
from elasticsearch import Elasticsearch

reponse = {"code":200,"msg":"success"}

class Question1(Resource):
    def get(self):
        # 建立elasticsearch連線
        es = Elasticsearch()
        # 獲取的資料條件 (DSL query)
        query_json = {
        "query": {
            "bool": {
            "must": [
                {"terms": {
                "性別要求": ["男女生皆可","男生"]
                }},
                {"wildcard":{
                    "地址":"新北市*"
                }},
            ]
            }
        }
        }
        query = es.search(index='houses',body=query_json,scroll='5m',size = 100)

        # 使用滾輪才能完整顯示每筆資料，否則elasticsearch會有資料數量限制
        results = query['hits']['hits'] # es查询出的结果第一页
        total = query['hits']['total']['value']  # es查询出的结果总量
        scroll_id = query['_scroll_id'] # 游标用于输出es查询出的所有结果
        for i in range(0, int(total/100)+1):
            # scroll参数必须指定否则会报错
            query_scroll = es.scroll(scroll_id=scroll_id,scroll='5m')['hits']['hits']
            results += query_scroll
        reponse['data'] = results
        return reponse

class Question2(Resource):
    def get(self,num):
        es = Elasticsearch()
        query_json = {
            "query": {
                "bool": {
                    "must": [
                        {"wildcard": {
                            "聯絡電話": num + '*'
                        }},
                    ]
                }
            }
        }
        query = es.search(index='houses', body=query_json, scroll='5m', size=100)
        results = query['hits']['hits']  # es查询出的结果第一页
        total = query['hits']['total']['value']  # es查询出的结果总量
        scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
        for i in range(0, int(total / 100) + 1):
            # scroll参数必须指定否则会报错
            query_scroll = es.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
            results += query_scroll
        reponse['data'] = results
        return reponse

class Question3(Resource):
    def get(self):
        es = Elasticsearch()
        query_json = {
            "query": {
                "bool": {
                    "must_not": [
                        {"terms": {
                            "出租者身份":["屋主*","屋主聲明：仲介勿擾"]
                        }},
                    ]
                }
            }
        }

        query = es.search(index='houses', body=query_json, scroll='5m', size=100)
        results = query['hits']['hits']  # es查询出的结果第一页
        total = query['hits']['total']['value']  # es查询出的结果总量
        scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
        for i in range(0, int(total / 100) + 1):
            # scroll参数必须指定否则会报错
            query_scroll = es.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
            results += query_scroll
        reponse['data'] = results
        print(len(results))
        return reponse

class Question4(Resource):
    def get(self):
        es = Elasticsearch()
        query_json = {
              "query": {
                "bool": {
                  "must": [
                    {"terms": {
                      "出租者": ["吳太太","吳媽媽","吳小姐","吳阿姨"]
                    }},
                     {"wildcard": {
                            "地址": "台北市*" }}
                  ]
                }
              }
            }

        query = es.search(index='houses',body=query_json,scroll='5m')
        print(query)
        results = query['hits']['hits'] # es查询出的结果第一页
        total = query['hits']['total']['value']  # es查询出的结果总量
        scroll_id = query['_scroll_id'] # 游标用于输出es查询出的所有结果

        for i in range(0, int(total/10)+1):
            # scroll参数必须指定否则会报错
            query_scroll = es.scroll(scroll_id=scroll_id,scroll='5m')['hits']['hits']
            results += query_scroll
        reponse['data']= results
        return reponse