from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from voidcms.models import Image


from voidcms.helpers.isAdmin import IsAdminUser


class ImageView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "DELETE"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise None

    def delete(self, request, pk):
        image = self.get_object(pk)
        if not image:
            return Response(status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
