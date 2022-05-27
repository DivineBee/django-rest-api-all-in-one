from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework import generics, permissions
from rest_framework.decorators import APIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from task.models import Product, Category
from task.serializers import ProductSerializer, CategorySerializer, ProductDocumentSerializer
from task.documents import ProductDocument
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


class UploadCategoryView(APIView):
    parser_classes = (JSONParser, MultiPartParser)

    def get(self, request):
        content = r'Submit File.'
        return Response(content, status=200)

    def post(self, request, *args, **kwargs):
        try:
            data = request.FILES.getlist('filename')[0].read()
            data = json.loads(data)
            request_details = {}

            if not data:
                content = "File is not uploaded !! Please upload a sample"
                return Response(content, status=500)

            for item in data:
                for k, v in item.items():
                    request_details['title'] = v
                requestsData = Category(title=request_details['title'], )
                requestsData.save()

            content = "File submitted successfully"
            return Response(content, status=200)

        except Exception as exp:
            content = {'Exception': 'Internal Error'}
            return Response(content, status=500)


class UploadProductView(APIView):
    parser_classes = (JSONParser, MultiPartParser)

    def get(self, request):
        content = r'Submit File.'
        return Response(content, status=200)

    def post(self, request, *args, **kwargs):
        try:
            data = request.FILES.getlist('filename')[0].read()
            data = json.loads(data)
            request_details = {}

            if not data:
                content = "File is not uploaded !! Please upload a sample"
                return Response(content, status=500)

            for item in data:
                for k, v in item.items():
                    request_details['title'] = item['title']
                    request_details['weight'] = item['weight']
                    request_details['price'] = item['price']
                    request_details['category'] = item['category']
                print(request_details)

                category = Category.objects.get(id=request_details['category'])
                requestsData = Product(title=request_details['title'], weight=request_details['weight'],
                                       price=request_details['price'], category=category,)
                requestsData.save()

            content = "File submitted successfully"
            return Response(content, status=200)

        except Exception as exp:
            content = {'Exception': 'Internal Error'}
            return Response(content, status=500)


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
    }
    # Specify default ordering
    ordering = ('id',)


class AuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You Are Authenticated', 'user': request.user.username})


class RegisterUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        User = get_user_model()
        user = User.objects.get(username=request.user.username)
        firebase_data = auth.get_user(user.username)
        user.email = firebase_data.email
        user.save()
        return Response({'message': 'User Registered'})