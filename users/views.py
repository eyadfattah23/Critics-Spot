from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer

# Create your views here.


@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('OK')


@api_view()
def user_details(request, id):
    user = get_object_or_404(CustomUser, pk=id)
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)
