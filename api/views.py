from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.http import HttpResponse

from api.models import Hero
from api.serializers import HeroSerializer


@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Hero.objects.all()
        serializer = HeroSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HeroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def snippet_detail(request,pk):

    try:
        snippet = Hero.objects.get(pk=pk)

    except Hero.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        snippets = Hero.objects.all()
        serializer = HeroSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = HeroSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
