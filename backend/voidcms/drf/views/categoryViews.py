from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


from voidcms.helpers.isAdmin import IsAdminUser

from voidcms.models import Category

from voidcms.drf.serializers.categorySerializer import CategorySerializer, CategoryTreeSerializer


def get_object(pk):
    try:
        return Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return None


class CategoryView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def get(self, request, pk=None):
        if pk is not None:
            category = get_object(pk)

            if not category:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = CategorySerializer(category)
            return Response(serializer.data)
        else:
            categories = Category.objects.filter(level=0)
            serializer = CategoryTreeSerializer(categories, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        category = get_object(pk)

        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object(pk)

        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryPositionView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.request.method in ["GET", "POST", "PUT", "DELETE"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def post(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            parent_id = request.data.get('parent_id')
            position = request.data.get('position')

            if parent_id == 'root':
                parent_category = None
            else:
                parent_category = Category.objects.get(pk=parent_id)

            wasNotEmpty = len(Category.objects.filter(parent=parent_category)) > 0

            category.move_to(parent_category, 'last-child')

            if wasNotEmpty:
                position = int(position)
                siblings = Category.objects.filter(parent=category.parent)
                lenSiblings = len(siblings)

                if position == 0:
                    target_sibling = siblings[position]
                    category.move_to(target_sibling, position='left')
                if position == (lenSiblings - 1):
                    target_sibling = siblings[position]
                    category.move_to(category.parent, position='last-child')
                if 0 < position < lenSiblings:
                    target_position = position

                    target_position = max(
                        0, min(target_position, lenSiblings - 1))

                    current_position = list(siblings).index(category)
                    if category.id != siblings[target_position].id:
                        if target_position < current_position:
                            category.move_to(
                                siblings[target_position], position='left')
                        else:
                            category.move_to(
                                siblings[target_position], position='right')

            return Response({'message': 'Position updated successfully'})
        except Category.DoesNotExist:
            return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
