from django.contrib.auth import authenticate, get_user_model

from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from django.http import HttpResponse

from api.models import Hero
from api.serializers import HeroSerializer

@api_view(['POST'])
# @authentication_classes([BasicAuthentication])
@permission_classes([AllowAny])
def login(request):
    # username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)



@api_view(['GET','POST'])
# @authentication_classes([BasicAuthentication])
@authentication_classes([TokenAuthentication])
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
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
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
