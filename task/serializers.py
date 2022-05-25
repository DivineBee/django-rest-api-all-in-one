from .models import Product, Category
from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .models import Product
from .documents import ProductDocument


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.ReadOnlyField(source='category.title')
    # category = Category.objects.get(title='category')

    class Meta:
        model = Product
        # read_only = True
        fields = ['id', 'title', 'weight', 'price', 'category']
        extra_kwargs = {
            'category': {'allow_null': True, 'required': False},
        }


class ProductDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ProductDocument
        fields = ['id', 'title', 'weight', 'price', 'category']
