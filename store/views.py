from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework import response, status, permissions, views
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.template.response import TemplateResponse


class HomePageView(views.APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve homepage data",
        operation_description="Returns a list of latest products and all categories for the homepage.",
        responses={
            200: 'HTML Template with products and categories'
        }
    )
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')[:20]
        categories = Category.objects.all()

        context = {
            'products': products,
            'categories': categories
        }
        return TemplateResponse(request, "home.html", context)

        
class ProductListCreateView(views.APIView):
    @swagger_auto_schema(responses={200: ProductSerializer(many=True)})
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderListCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


