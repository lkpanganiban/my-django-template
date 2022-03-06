from elasticsearch_dsl import analyzer

file_analyzer = analyzer(
    'file_analyzer',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"]
)