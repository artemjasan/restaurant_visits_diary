from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from v1.diary.models import Visit
from v1.diary.permissions import IsCreator
from v1.diary.serializers import visit_serializers


class VisitList(generics.ListAPIView):
    serializer_class = visit_serializers.VisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return Visit.objects.filter(creator=self.request.user)


class VisitDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = visit_serializers.VisitSerializer
    permission_classes = [IsAuthenticated, IsCreator]
