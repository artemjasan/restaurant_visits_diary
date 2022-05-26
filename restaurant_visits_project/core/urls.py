from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


schema_patterns = [
    path(route="download/", view=SpectacularAPIView.as_view(), name="schema"),
    path(route="swagger-ui/", view=SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(route="redoc/", view=SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


auth_patterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
]

api_v1_patterns = [path("v1/", include("v1.urls")), path("auth/", include([*auth_patterns]))]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                *api_v1_patterns,
                path("schema/", include(schema_patterns)),
            ]
        ),
    ),
]
