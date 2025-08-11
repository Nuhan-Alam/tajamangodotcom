from django.urls import path,include
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet, ProductImageViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)

product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
product_router.register('images', ProductImageViewSet,basename='product-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]