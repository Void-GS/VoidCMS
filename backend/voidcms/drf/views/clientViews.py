from django.contrib.auth import get_user_model, logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from voidcms.drf.serializers.clientSerializer import ClientSerializer, EmailLoginSerializer
from voidcms.helpers.isAdmin import IsAdminUser
from voidcms.models import Client


User = get_user_model()


class LogoutView(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({"success": "Successfully logged out"})
        else:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class RegisterView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"success": "Registration successful"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    serializer_class = EmailLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class GetAuthUserView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = request.user

        serializer = ClientSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientsView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.request.method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise None

    def get(self, request, pk=None):
        if pk is not None:
            client = self.get_object(pk)

            if not client:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = ClientSerializer(client)
            return Response(serializer.data)
        else:
            clients = Client.objects.all()
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data)

    def delete(self, request, pk):
        if request.user.pk != pk:
            client = self.get_object(pk)

            if not client:
                return Response(status=status.HTTP_404_NOT_FOUND)

            client.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def patch(self, request, pk):
        if request.user.pk != pk:
            client = self.get_object(pk)

            if not client:
                return Response(status=status.HTTP_404_NOT_FOUND)

            new_role = request.data.get('role')

            if new_role is not None:
                client.role = new_role
                client.save()
                serializer = ClientSerializer(client)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
