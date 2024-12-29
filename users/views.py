from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, Favorite
from .serializers import CustomUserSerializer, UserCreateSerializer
from .serializers import FavoriteSerializer
from rest_framework import status

# Create your views here.


@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.prefetch_related('shelves').all()
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
    user = get_object_or_404(CustomUser, pk=pk)
    serializer = CustomUserSerializer(user, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def user_favorites(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    favorites = Favorite.objects.filter(user=user)
    if request.method == 'POST':
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    serilizer = FavoriteSerializer(favorites, many=True, context={'request': request})
    return Response(serilizer.data)


@api_view(['GET', 'DELETE'])
def favorite_detail(request, pk, favorite_pk):
    user = get_object_or_404(CustomUser, pk=pk)
    favorite = get_object_or_404(Favorite, user=user, pk=favorite_pk)
    if request.method == 'GET':
        serializer = FavoriteSerializer(favorite, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'DELETE':
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
