from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, UserCreateSerializer
from rest_framework import status

# Create your views here.


@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def user_details(request, pk):
    user = get_object_or_404(
        CustomUser,
        pk=pk
    )
    serializer = CustomUserSerializer(user, context={'request': request})
    return Response(serializer.data)
