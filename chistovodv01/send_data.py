from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['https://34f88794695f4fdaf93f7a2ee885da16.eu-west-1.aws.found.io'],
    http_auth=('ayrat', 'qweqwe1'),
    port=443,
    use_ssl=True)
print(es.info())


INDEX_NAME = 'test'
if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))
# since we are running locally, use one shard and no replicas
request_body = {
    "settings" : {
        "number_of_shards": 5,
        "number_of_replicas": 0
    }
}
print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))

print("bulk indexing...")
res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)

# sanity check
res = es.search(index = INDEX_NAME, size=2, body={"query": {"match_all": {}}})
print(" response: '%s'" % (res))

bulk_data[0], bulk_data[1]