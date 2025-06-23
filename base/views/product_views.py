from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.products import products
from base.models import *
from base.serializers import ProductSerializer

# Create your views here.
from rest_framework import status




@api_view(['GET'])
def getProducts(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set, many= True)
    return Response(serializer.data)
    # return Response(products)


@api_view(['GET'])
def getProduct(request, pk):
    query_set = Product.objects.get(_id=pk)
    serializer = ProductSerializer(query_set, many = False)
    return Response(serializer.data) 