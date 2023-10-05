from rest_framework.views import APIView
from django.db.models import Q, F, ExpressionWrapper, FloatField
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


from voidcms.helpers.isAdmin import IsAdminUser
from rest_framework.permissions import AllowAny

from voidcms.models import Product
from voidcms.models import Category

from voidcms.drf.serializers.productSerializer import ProductSerializer

class ProductView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get_object_meta(self, meta_url):
        try:
            return Product.objects.get(meta_url=meta_url, visible=True)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk is not None:
            product = self.get_object(pk)

            if not product:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product)
            return Response(serializer.data)

        category_url = request.GET.get('category_url')
        meta_url = request.GET.get('meta_url')
        page_number = request.GET.get('page', 1)
        all = request.GET.get('all', 'false')
        sort_price = request.GET.get('sort_price')

        if meta_url:
            product = self.get_object_meta(meta_url)

            if not product:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # Wrap the product in a list
            serializer = ProductSerializer([product], many=True)
            return Response(serializer.data)

        if all == 'true':
            processedProducts = Product.objects.all()
        else:
            processedProducts = Product.objects.filter(visible=True)

        if category_url:
            category = Category.objects.get(meta_url=category_url)

            if not category:
                return Response({'message': 'Category Not Found'}, status=status.HTTP_404_NOT_FOUND)
            
            descendant_categories = category.get_descendants(include_self=True)
            processedProducts = processedProducts.filter(category__in=descendant_categories)
        
        if sort_price == 'desc':
            processedProducts = processedProducts.annotate(
                calculated_price=ExpressionWrapper(F('price'), output_field=FloatField())
            ).order_by('calculated_price')
        elif sort_price == 'asc':
            processedProducts = processedProducts.annotate(
                calculated_price=ExpressionWrapper(F('price'), output_field=FloatField())
            ).order_by('-calculated_price')
            
        paginator = Paginator(processedProducts[::-1], 20)
        total_pages = paginator.num_pages

        try:
            page = paginator.page(page_number)

            if not page:
                return Response([])

            serializer = ProductSerializer(page, many=True)
            response_data = serializer.data
            response = Response(response_data, status=status.HTTP_200_OK)
            response['X-Total-Pages'] = total_pages
            response['X-Current-Page'] = page.number
            return response
        except EmptyPage:
            return Response({'error': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = self.get_object(pk)

        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)

        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()

        return Response(status=status.HTTP_202_ACCEPTED)
    

class ProductPromotedView(APIView):
    def get(self, request):
            promoted = Product.objects.filter(is_promoted=True)[::-1][:5]
            serializer = ProductSerializer(promoted, many=True)
            return Response(serializer.data)

