from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from .models import CustomUser, Favorite
from .serializers import *
from .filters import CustomUserFilter, BookReviewFilter
# Create your views here.


class CustomUserList(ListCreateAPIView):
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CustomUserFilter
    search_fields = ['username', 'first_name', 'last_name', 'email']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return CustomUserSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get(self, request, *args, **kwargs):
        self.serializer_class = CustomUserSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        return self.create(request, *args, **kwargs)


class CustomUserDetails(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    serializer_class = CustomUserSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET', 'POST'])
def user_favorites(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    favorites = Favorite.objects.filter(user=user)
    if request.method == 'POST':
        serializer = FavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    serilizer = FavoriteSerializer(
        favorites, many=True, context={'request': request})
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


class BookReviewsList(ListCreateAPIView):
    serializer_class = BookReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BookReviewFilter
    search_fields = ['content']

    def get_queryset(self):
        book_id = self.kwargs['pk']
        book = get_object_or_404(Book, pk=book_id)
        return BookReview.objects.filter(book=book)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        book_id = self.kwargs['pk']
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(book=book)


class BookReviewDetails(RetrieveUpdateDestroyAPIView):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer

    def get_serializer_context(self):
        return {'request': self.request}
