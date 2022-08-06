from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from .analyzers import file_analyzer
from .models import Files

@registry.register_document
class FilesDocument(Document):
    name = fields.TextField(analyzer=file_analyzer)
    owner = fields.KeywordField(
        attr = 'get_owner',
    )
    file_type = fields.KeywordField()
    file_size = fields.IntegerField()
    description = fields.TextField()
    file_set = fields.TextField(
        attr = 'get_file_set',
    )

    class Index:
        name = 'files'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Files
        fields = ['id']