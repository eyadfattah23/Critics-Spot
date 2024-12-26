from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shelf
from .serilizers import ShelfSerializer


@api_view()
def shelves_list(request):
    """ Return all the shelves. """
    shelves = Shelf.objects.all()
    serilizer = ShelfSerializer(shelves, many=True)
    return Response(serilizer.data)


@api_view()
def shelf_details(request, id):
    """ Return the users shelves from the id of the user. """
    shelf = get_object_or_404(Shelf, pk=id)
    serilizer = ShelfSerializer(shelf)
    return Response(serilizer.data)
