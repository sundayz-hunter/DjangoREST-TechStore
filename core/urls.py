from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView, SpectacularAPIView

from core import settings
from user.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include('api_v1.urls')),
    path('silk/', include('silk.urls', namespace='silk')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
