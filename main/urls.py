from django.urls import path
from . import views
urlpatterns = [
    path('', views.ProductListView.as_view(), name='main'),
    path('test/', views.TestTemplateView.as_view()),
    path('<int:pk>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/', views.detail_cart, name='cart_detail')
]
