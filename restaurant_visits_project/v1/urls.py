from django.urls import include, path

from .diary.urls import urlpatterns

urlpatterns = [
    path("", include(urlpatterns)),
]
