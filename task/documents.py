from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
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


# @registry.register_document
@INDEX.doc_type
class ProductDocument(Document):
    html_strip = analyzer(
        'html_strip',
        tokenizer="standard",
        filter=["standard", "lowercase", "stop", "snowball"],
        char_filter=["html_strip"]
    )

    id = fields.IntegerField(attr='id')

    title = fields.ObjectField(
        analyzer=html_strip,
        fields={
            'raw': fields.ObjectField(analyzer='keyword'),
        }
    )
    weight = fields.FloatField()
    price = fields.FloatField()
    category = fields.ObjectField(
        attr='category_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.ObjectField(analyzer='keyword'),
        }
    )
    # category = fields.ObjectField(properties={
    #     'title': fields.TextField()
    # })

    # class Index:
    #     name = 'products'
    #     # indexes are subdivided into multiple instances called shards
    #     # replicas are copies of shards
    #     settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Product

        # fields = [
        #     'title',
        #     'weight',
        #     'price',
        # ]
        #
        # related_models = [Category]

