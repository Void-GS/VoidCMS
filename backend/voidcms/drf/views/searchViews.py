from voidcms.models import Category, Product
from voidcms.drf.serializers.categorySerializer import CategorySerializer
from voidcms.drf.serializers.productSerializer import ProductSerializer
from voidcms.drf.serializers.searchSerializer import SearchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q


class SearchView(APIView):
    def get(self, request):
        serializer = SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data['query'].lower()

        # Create a mapping function to map characters from any language to Russian keyboard
        def keyboard_mapping(char):
            mapping = {
                'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е',
                'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
                'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п',
                'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж',
                "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м',
                'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю',
            }
            return mapping.get(char, char)

        query = ''.join(map(keyboard_mapping, query))

        all_categories = Category.objects.all()
        filtered_categories = []

        for category in all_categories:
            if query in category.title.lower() or query in category.description.lower():
                filtered_categories.append(category)

        filtered_categories = filtered_categories[::-1][:10]

        all_products = Product.objects.filter(visible=True)
        filtered_products = []

        for product in all_products:
            if query in product.title.lower() or query in product.content.lower():
                filtered_products.append(product)

        filtered_products = filtered_products[::-1][:15]

        category_serialized = CategorySerializer(
            filtered_categories, many=True)
        product_serialized = ProductSerializer(filtered_products, many=True)

        response_data = {
            'categories': category_serialized.data,
            'products': product_serialized.data
        }

        return Response(response_data)
