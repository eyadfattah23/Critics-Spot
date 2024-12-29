from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shelf
from users.models import CustomUser
from .serializers import ShelfSerializer, UserSerializer


@api_view(['GET'])
def shelves_list(request):
    """ Return all the shelves. """
    shelves = Shelf.objects.select_related('user').prefetch_related('shelfbook_set__book').all()
    serializer = ShelfSerializer(shelves, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def shelf_details(request, id):
    """ Return the users shelves from the id of the user. """
    shelf = get_object_or_404(Shelf.objects.prefetch_related('shelfbook_set__book'), pk=id)
    serializer = ShelfSerializer(shelf, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def user_details(request, pk):
    """ Return the users of shelves from the id of the user. """
    user = get_object_or_404(CustomUser, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)
