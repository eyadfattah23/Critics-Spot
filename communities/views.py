from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Community
from .serializers import CustomCommunitySerializer


@api_view()
def communities_list(request):
    """ Return all the communities. """
    communities = Community.objects.prefetch_related('members').all()
    serializer = CustomCommunitySerializer(communities, many=True, context={'request': request})
    return Response(serializer.data)


@api_view()
def community_details(request, id):
    """Return the details of a specific community. """
    return Response(id)
