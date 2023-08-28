from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', admin.site.urls),
    path("api/", include("buildings.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("users/", include("users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
