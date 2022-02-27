from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Files

@registry.register_document
class FilesDocument(Document):
    class Index:
        name = 'files'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
    
    owner = fields.TextField(attr = 'get_owner')
    class Django:
        model = Files
        fields = [
            'name',
            'file_type',
            'file_size',
            'location',
        ]