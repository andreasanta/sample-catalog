from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('products/<str:pk>/', ProductDetailView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)