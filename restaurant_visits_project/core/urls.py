
from django.contrib import admin
from django.urls import include, path

api_v1_patterns = [
    path("v1/", include("v1.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include([*api_v1_patterns])),
]
