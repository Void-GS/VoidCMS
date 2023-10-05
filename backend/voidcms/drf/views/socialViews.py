from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from voidcms.drf.serializers.socialSerializer import SocialSerializer
from voidcms.models import Social
from voidcms.helpers.isAdmin import IsAdminUser


class SocialView(APIView):
    parser_classes = (MultiPartParser,FormParser,JSONParser)

    
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def get_object(self, pk):
        try:
            if pk:
                return Social.objects.get(pk=pk)
        except Social.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is not None:
            social = self.get_object(pk)

            if not social:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = SocialSerializer(social)
            return Response(serializer.data)
        else:
            socials = Social.objects.all()
            serializer = SocialSerializer(socials, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = SocialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):    
        social = self.get_object(pk)

        if not social:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = SocialSerializer(social, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        social = self.get_object(pk)
        if not social:
                return Response(status=status.HTTP_404_NOT_FOUND)
        social.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
