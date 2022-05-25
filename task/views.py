from rest_framework import generics, permissions
from task.models import Product, Category
from task.serializers import ProductSerializer, CategorySerializer, ProductDocumentSerializer
from task.documents import ProductDocument
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)

# List all products
class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer  # reference to serializer class
    permission_classes = [permissions.IsAuthenticated]  # allow only authenticated users

    def get_queryset(self):  # without a defined query set it will not work
        return Product.objects.order_by('title')  # order products by their title


# CRUD per product. Handled completely by the rest framework.
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.order_by('title')


# List all categories
class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.order_by('title')


# CRUD per category
class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.order_by('title')


class ProductDocumentViewElasticSearch(BaseDocumentViewSet):
    document = ProductDocument
    serializer_class = ProductDocumentSerializer
    lookup_field = 'id'

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        'id', 'title',
    )

    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'title': 'title.raw',
        'weight': {
            'field': 'weight',
            # Note, that we limit the lookups of `weight` field in this
            # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'price': 'price',
        'category': 'category.raw'
    }

    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        # 'title': 'title.raw',
        # 'price': 'price',
    }
    # Specify default ordering
    ordering = ('id',)
    # ordering = ('id', 'title', 'price',)

