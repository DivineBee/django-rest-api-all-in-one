from django.urls import path
from .views import ProductRetrieveUpdateDestroy, ProductList, CategoryRetrieveUpdateDestroy, CategoryList

app_name = 'task'

urlpatterns = [
    path('product_list/', ProductList.as_view()),
    path('category_list/', CategoryList.as_view()),
    path('product_list/<int:pk>', ProductRetrieveUpdateDestroy.as_view()),
    path('category_list/<int:pk>', CategoryRetrieveUpdateDestroy.as_view()),
]
