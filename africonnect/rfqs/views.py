from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import RFQ
from rest_framework.generics import GenericAPIView
from rest_framework.generics import CreateAPIView
from .serializers import RFQSerializer
from .serializers import RFQFormConfigSerializer


class RFQFormConfigView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = RFQFormConfigSerializer

    def get(self, request):

        data = {
            "product_categories": [
                {"value": category[0], "label": category[1]}
                for category in RFQ.CATEGORY_CHOICES
            ],
            "units": [
                {"value": unit[0], "label": unit[1]} for unit in RFQ.UNIT_CHOICES
            ],
        }

        return Response(data)


class RFQCreateView(CreateAPIView):

    queryset = RFQ.objects.all()

    serializer_class = RFQSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(buyer=self.request.user)
