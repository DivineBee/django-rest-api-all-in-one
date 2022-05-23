from rest_framework import generics, permissions
from task.models import Product, Category
from task.serializers import ProductSerializer, CategorySerializer

# List all products
class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer  # reference to serializer class
    permission_classes = [permissions.IsAuthenticated]  # allow only authenticated users

    def get_queryset(self): # without a defined query set it will not work
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