"""
URL configuration for tortas-crispan-backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="SISGETC API",
      default_version='v1',
      description="Documentation API SISGETC",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="liseth.castillo@correounivalle.edu.co"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Swagger
    path('api/docs/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Django Admin
    path('admin/', admin.site.urls),
    # APPS URLS
    path('', include(('apps.users.urls', 'users'), namespace='users')),
    path('', include(('apps.purchases.urls', 'purchases'), namespace='purchases')),
    path('', include(('apps.sales.urls', 'sales'), namespace='sales')),
    path('', include(('apps.utils.urls', 'utils'), namespace='utils')),
    path('', include(('apps.reports.urls', 'reports'), namespace='reports')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
