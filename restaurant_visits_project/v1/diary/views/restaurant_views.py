from django.db.models import Avg, QuerySet
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from v1.diary.models import Restaurant
from v1.diary.permissions import IsCreator
from v1.diary.serializers import restaurant_serializers, visit_serializers


class RestaurantList(generics.ListCreateAPIView):
    serializer_class = restaurant_serializers.RestaurantListSerializer

    def get_queryset(self) -> QuerySet:
        return (
            Restaurant.visited_objects.filter(creator=self.request.user)
            .annotate(_average_rating=Avg("visits__rating"))
            .order_by("-id")
        )


class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = restaurant_serializers.RestaurantDetailSerializer
    permission_classes = [IsCreator]


class AddVisitToRestaurant(generics.GenericAPIView):
    serializer_class = visit_serializers.BaseVisitSerializer
    permission_classes = [IsCreator]
    queryset = Restaurant.objects.all()

    def post(self, request: Request, *args, **kwargs) -> Response:
        restaurant = self.get_object()
        serializer = visit_serializers.BaseVisitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        visit = serializer.save(creator=request.user, restaurant=restaurant)
        restaurant.visits.add(visit)
        return Response(f"A new visit to {restaurant.name} restaurant was added.", status=status.HTTP_201_CREATED)
