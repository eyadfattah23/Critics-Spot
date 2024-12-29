from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def communities_list(request):
    """ Return all the shelves. """
    return Response("Hello, World!")


@api_view()
def community_details(request, id):
    """ Return the users shelves from the id of the user. """
    return Response(id)
