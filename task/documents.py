from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from .models import Product, Category
from django.conf import settings

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
        'html_strip',
        tokenizer="standard",
        filter=["standard", "lowercase", "stop", "snowball"],
        char_filter=["html_strip"]
    )


# @registry.register_document
@INDEX.doc_type
class ProductDocument(Document):

    id = fields.IntegerField(attr='id')

    title = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )
    weight = fields.FloatField()
    price = fields.FloatField()
    category = fields.TextField(
        attr='category_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    class Django:
        model = Product

