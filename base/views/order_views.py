from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.products import products
from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import OrderSerializer

# Create your views here.
from rest_framework import status


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data["orderItems"]

    if orderItems and len(orderItems) == 0:
        return Response(
            {"detail": "no order items"}, status=status.HTTP_400_BAD_REQUEST
        )
    else:
        # (1)create order
        order = Order.objects.create(
            user=user,
            paymentMethod=data["paymentMethod"],
            taxPrice=data["taxPrice"],
            shippingPrice=data["shippingPrice"],
            totalPrice=data["totalPrice"],
        )

        # (2)create shipping address
        shippingAddress = ShippingAddress.objects.create(
            order=order,
            address=data["shippingAddress"]["address"],
            city=data["shippingAddress"]["city"],
            postalCode=data["shippingAddress"]["postalCode"],
            country=data["shippingAddress"]["country"],
        )

        # (3)create order items and set order to orderItem relation
        for i in orderItems:
            product = Product.objects.get(_id=i["product"])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i["qty"],
                price=i["price"],
                image=product.image.url,
            )

        # (4)update stock
        product.countInStock -= item.qty
        product.save()

        serializer = OrderSerializer(order, many=False)

        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrderItems(request, pk):
    user = request.user
    order = Order.objects.get(_id=pk)

    try:
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response(
                {"details": "not authorized to view this order"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except:
        return Response(
            {"details": "Order does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )
