from django.contrib import admin
from django.urls import path,include
from .views import api_root_view
from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="TajaMangoDotCom-API",
      default_version='v1',
      description="This project is a full-featured online marketplace dedicated to mango sales. Sellers can create detailed listings with images, descriptions, and prices, while buyers can browse, purchase instantly, and track orders through personal accounts. An admin dashboard will oversee listings and orders, ensuring smooth, secure, and efficient transactions.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root_view),
    path('api/v1/',include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + debug_toolbar_urls()
