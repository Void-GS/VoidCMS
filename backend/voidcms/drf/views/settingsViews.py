from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from voidcms.drf.serializers.settingsSerializer import SettingsSerializer
from voidcms.models import Settings
from voidcms.helpers.isAdmin import IsAdminUser


class SettingsView(APIView):
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
                return Settings.objects.get(pk=pk)
        except Settings.DoesNotExist:
            return None
        
    def get_object_meta(self, app_url):
        try:
            return Settings.objects.get(app_url=app_url)
        except Settings.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is not None:
            settings = self.get_object(pk)
            serializer = SettingsSerializer(settings)
            return Response(serializer.data)
        else:
            app_url = request.GET.get('app_url')
            if app_url:
                settings = self.get_object_meta(app_url)
                if not settings:
                    return Response([])
                else:
                    serializer = SettingsSerializer([settings], many=True)
                    return Response(serializer.data)

            settings = Settings.objects.all()
            serializer = SettingsSerializer(settings, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = SettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):    
        settings = self.get_object(pk)

        if not settings:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        settings = self.get_object(pk)
        if not settings:
            return Response(status=status.HTTP_404_NOT_FOUND)
        settings.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
