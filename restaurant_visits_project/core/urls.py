
from django.contrib import admin
from django.urls import include, path

auth_patterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
]

api_v1_patterns = [
    path("v1/", include("v1.urls")),
    path("auth/", include([*auth_patterns]))
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include([*api_v1_patterns])),
]
