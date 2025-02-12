from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .models import Product
from django.shortcuts import get_object_or_404

from rest_framework import generics, filters
from .serializers import ProductSerializer



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        product = get_object_or_404(Product, pk=pk, owner=request.user)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        product = get_object_or_404(Product, pk=pk, owner=request.user)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        product = get_object_or_404(Product, pk=pk, owner=request.user)
        product.delete()
        return Response({"message": "Mahsulot o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)
