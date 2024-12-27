from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Community
from .serializers import CustomCommunitySerializer, PostSerializer, Post


@api_view()
def communities_list(request):
    """ Return all the communities. """
    communities = Community.objects.prefetch_related('members', 'owner').all()
    serializer = CustomCommunitySerializer(
        communities,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view()
def community_details(request, pk):
    """Return the details of a specific community. """
    community = get_object_or_404(Community, pk=pk)
    serializer = CustomCommunitySerializer(
        community,
        context={'request': request})
    return Response(serializer.data)


@api_view()
def community_posts(request, pk):
    """Return the posts of a specific community. """
    community = get_object_or_404(Community, pk=pk)
    posts = Post.objects.filter(community=community)
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)
