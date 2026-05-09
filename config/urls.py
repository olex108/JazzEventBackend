from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import debug_toolbar
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("content.urls", namespace="content")),
    path("", include("users.urls", namespace="users")),
]

if settings.DEBUG:


    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
