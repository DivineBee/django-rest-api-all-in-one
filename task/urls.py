from django.urls import path, include
from .views import ProductRetrieveUpdateDestroy, ProductList, \
    ProductDocumentViewElasticSearch, CategoryRetrieveUpdateDestroy, CategoryList
from rest_framework.routers import DefaultRouter

app_name = 'task'

router = DefaultRouter()
product = router.register(r'product',
                          ProductDocumentViewElasticSearch,
                          basename='productdocument')

urlpatterns = [
    path('product_list/', ProductList.as_view()),
    path('category_list/', CategoryList.as_view()),
    path('product_list/<int:pk>', ProductRetrieveUpdateDestroy.as_view()),
    path('category_list/<int:pk>', CategoryRetrieveUpdateDestroy.as_view()),
    path(r'search/', include(router.urls)),
]

# urlpatterns += router.urls
