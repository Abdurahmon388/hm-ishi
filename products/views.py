from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.http import HttpResponse
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics, filters, status

from django.http import JsonResponse
from django.views import View


class ProductView(View):

    @staticmethod
    def get_products():
        return list(Product.objects.values())

    def get(self, request):
        products = self.get_products()
        return JsonResponse({"products": products})


class ProductListCreateAPIView(APIView):

    @staticmethod
    def get_products():
        """Mahsulotlar ro‘yxatini qaytaruvchi yordamchi metod"""
        return Product.objects.all()

    def get(self, request):
        products = self.get_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductBySlugView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]


def product_list(request):
    return HttpResponse("Bu mahsulotlar ro‘yxati sahifasi!")



class ProductAPIView(APIView):
    @staticmethod
    def get(request):
        return Response({"message": "Product API ishlayapti"})


class UserProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)
