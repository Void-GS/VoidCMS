from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from voidcms.drf.serializers.pageSerializer import PageSerializer
from voidcms.models import Page
from voidcms.helpers.isAdmin import IsAdminUser


class PageView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def get_object(self, pk=None, meta_url=None):
        try:
            if pk:
                return Page.objects.get(pk=pk)
            elif meta_url:
                return Page.objects.get(meta_url=meta_url)
        except Page.DoesNotExist:
            return None

    def get(self, request, pk=None):
        all = request.GET.get('all', False)

        if pk is not None:
            page = self.get_object(pk)

            if not page:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = PageSerializer(page)
            return Response(serializer.data)
        else:
            meta_url = request.GET.get('meta_url')
            if meta_url:
                page = self.get_object(meta_url=meta_url)

                if not page:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = PageSerializer(page)
                return Response(serializer.data)
            
            if all:
                pages = Page.objects.all()
            else:
                pages = Page.objects.filter(visible=True)
            serializer = PageSerializer(pages, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = PageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        page = self.get_object(pk)

        if not page:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PageSerializer(page, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        page = self.get_object(pk)
        if not page:
            return Response(status=status.HTTP_404_NOT_FOUND)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
