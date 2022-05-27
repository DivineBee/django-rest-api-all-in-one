from django.urls import path, include
from .views import ProductRetrieveUpdateDestroy, ProductList, UploadCategoryView, \
    ProductDocumentViewElasticSearch, CategoryRetrieveUpdateDestroy, CategoryList, UploadProductView,\
    AuthenticatedView, RegisterUser
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
    path(r'upload-category/', UploadCategoryView.as_view()),
    path(r'upload-product/', UploadProductView.as_view()),
    path('verified', AuthenticatedView.as_view()),
    path('register', RegisterUser.as_view()),
]

