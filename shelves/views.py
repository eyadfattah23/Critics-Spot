from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shelf
from users.models import CustomUser
from .serializers import ShelfSerializer, ShelfCreateSerializer


@api_view(['GET'])
def shelves_list(request):
    """ Return all the shelves. """
    shelves = Shelf.objects.select_related('user').prefetch_related('shelfbook_set__book').all()
    serializer = ShelfSerializer(shelves, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def shelf_details(request, pk):
    """ Return the users shelves from the id of the user. """
    shelf = get_object_or_404(Shelf.objects.prefetch_related('shelfbook_set__book'), pk=pk)
    serializer = ShelfSerializer(shelf, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def create_shelf(request, user_id):
    """ Create a new shelf. """
    user = get_object_or_404(CustomUser, pk=user_id)
    data = request.data.copy()
    data['user'] = user.id
    serializer = ShelfCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=user)
    return Response(serializer.data)
