from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from django.contrib.auth.models import User

from base.models import *
from base.serializers import UserSerializer, UserSerializerWithToken

# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status


# user token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     token['name'] = user.username
    #     token['message'] = 'Hello world'

    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add your extra responses here
        # data['username'] = self.user.username
        # data['email'] = self.user.email
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# user register


@api_view(["POST"])
def registerUser(request):
    data = request.data
    print("Data:", data)

    try:
        user = User.objects.create(
            first_name=data["name"],
            username=data["email"],
            email=data["email"],
            password=make_password(data["password"]),
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {"detail": "user with this email already exist"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "post"])
def getRoutes(request):
    routes = [
        "api/products/",
        "api/products/create",
        "api/products/upload",
    ]
    return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# @api_view(["PUT"])
# @permission_classes([IsAuthenticated])
# def updateUserProfile(request):
#     user = request.user
#     serializer = UserSerializerWithToken(user, many=False)

#     data = request.data
#     user.first_name = data["name"]
#     user.user_name = data["email"]
#     user.email = data["email"]

#     # if 'password' in request.data and request.data['password'] != '':
#     #     user.password = make_password(request.data['password'])


#     if(data['password'] != ""):
#         user.password = make_password(data['password'])

#     user.save()
#     return Response(serializer.data)


# @api_view(["PUT"])
# @permission_classes([IsAuthenticated])
# def updateUserProfile(request):
#     user = request.user
#     serializer = UserSerializerWithToken(user, many=False)

#     data = request.data
#     user.first_name = data["name"]
#     user.username = data["email"]
#     user.email = data["email"]

#     if 'password' in data and data['password'] != '':
#         user.password = make_password(data['password'])

#     user.save()

#     return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data.get("name", user.first_name)
    user.username = data.get("email", user.username)
    user.email = data.get("email", user.email)

    password = data.get('password', None)
    if password:
        user.password = make_password(password)

    user.save()
    return Response(serializer.data)
