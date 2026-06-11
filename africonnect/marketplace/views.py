from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from products.models import Product, ProductCategory
from profiles.models import SupplierProfile

from .serializers import (
    MarketplaceProductSerializer,
    MarketplaceProductDetailSerializer,
    MarketplaceCategorySerializer,
    MarketplaceSupplierSerializer,
    MarketplaceSupplierDetailSerializer,
    CountryListSerializer,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .constants import COUNTRIES

from common.serializers import CategorySerializer

class MarketplaceProductListView(ListAPIView):

    permission_classes = [AllowAny]

    serializer_class = MarketplaceProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = {
        "country": ["exact"],
        "category_id": ["exact"],
    }
    

    search_fields = [
        "name",
        "business_name",
    ]

    ordering_fields = [
        "price",
        "created_at",
    ]

    ordering = [
        "-created_at"
    ]


    def get_queryset(self):

        return Product.objects.filter(
            is_public=True,
            supplier__is_public=True
        ).select_related(
            "supplier",
            "category",
        )


class MarketplaceProductDetailView(RetrieveAPIView):

    permission_classes = [AllowAny]

    serializer_class = MarketplaceProductDetailSerializer

    lookup_field = "id"

    def get_queryset(self):

        return Product.objects.filter(
            is_public=True,
            supplier__is_public=True
        ).select_related(
            "supplier",
            "category",
        )







class MarketplaceSupplierListView(ListAPIView):

    permission_classes = [AllowAny]

    serializer_class = MarketplaceSupplierSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    
    filterset_fields = {
        "country": ["exact"],
        "verified": ["exact"],
    }

    search_fields = [
        "business_name",      
    ]

    ordering_fields = [
        "rating",
        "created_at",
    ]

    ordering = [
        "-rating"
    ]

    def get_queryset(self):

        return SupplierProfile.objects.filter(
            is_public=True
        )
        
        
class MarketplaceSupplierDetailView(RetrieveAPIView):

    permission_classes = [AllowAny]
    serializer_class = MarketplaceSupplierDetailSerializer

    queryset = SupplierProfile.objects.filter(
        is_public=True
    )

        

class MarketplaceCategoryListView(ListAPIView):

    permission_classes = [AllowAny]

    serializer_class = CategorySerializer

    def get_queryset(self):

        return ProductCategory.objects.all()   
    
    
    
    
#class CountryListView(APIView):

    #permission_classes = [AllowAny]

    #def get(self, request):

        #return Response({
            #"countries": COUNTRIES
        #})    
    



class CountryListView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = CountryListSerializer

    def get(self, request):

        return Response({
            "countries": COUNTRIES
        })         

# Create your views here.
