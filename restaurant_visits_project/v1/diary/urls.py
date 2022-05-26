from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from v1.diary.views import crypto_views, restaurant_views, visit_views

urlpatterns = [
    path("visits/", visit_views.VisitList.as_view()),
    path("visits/<int:pk>/", visit_views.VisitDetail.as_view()),
    path("restaurants/", restaurant_views.RestaurantList.as_view()),
    path("restaurants/<int:pk>/", restaurant_views.RestaurantDetail.as_view()),
    path("restaurants/<int:pk>/add_visit/", restaurant_views.AddVisitToRestaurant.as_view()),
    path("crypto/", crypto_views.CryptoViews.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
