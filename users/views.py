from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer

# Create your views here.


@api_view()
def users_list(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view()
def user_details(request, id):
    try:
        user = CustomUser.objects.get(pk=id)
        serializer = CustomUserSerializer(user)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    return Response(serializer.data)
