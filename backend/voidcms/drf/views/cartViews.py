from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from voidcms.models import Cart, CartItem
from voidcms.drf.serializers.cartSerializer import CartSerializer, CartItemSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return None

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            cart = self.get_object(pk=user)
            if not cart:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        else:
            raise Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        id = request.data.get('id')
        product_id = request.data.get('product_id')
        complectations = request.data.get('complectations', [])
        count = request.data.get('count', 1)

        cart = self.get_object(pk=user)

        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = CartItem.objects.get(product_id=product_id, cart=cart, complectations=complectations)
            cart_item.count += count
            cart_item.save()            
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product_id=product_id, complectations=complectations, count=count)
            cart.items.add(cart_item)

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        user = request.user
        id = request.data.get('id')

        try:
            cart_item = CartItem.objects.get(id=id)
            cart_item.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_202_ACCEPTED)
