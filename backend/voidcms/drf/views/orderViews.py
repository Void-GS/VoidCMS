from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from voidcms.helpers.isAdmin import IsAdminUser

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


from voidcms.models import Order, OrderItem, OrderProduct, Product, Cart
from voidcms.drf.serializers.orderSerializer import OrderSerializer, OrderItemSerializer


class OrderView(APIView):
    parser_classes = (MultiPartParser,FormParser,JSONParser)

    
    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated()]
        elif self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def collect_orderItems(self, items):
        order_items = []
        for item in items:
            product_id = item['product']['id']
            product_instance = Product.objects.get(id=product_id)
            order_product = OrderProduct.objects.create(title=product_instance.title, price=product_instance.price, meta_url=product_instance.meta_url)
            order_item = OrderItem.objects.create(product=order_product, complectations=item['complectations'], count=item['count'])
            print('==========')
            print(OrderItemSerializer(order_item).data)
            print('==========')
            order_items.append(order_item)
        return order_items

    def get(self, request, pk=None):
        user = request.user
        if pk is not None:
            order = self.get_object(pk)

            if not order:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if order.client.id != user.id and not IsAdminUser():
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            all = request.GET.get('all', False)
            if all and IsAdminUser():
                orders = Order.objects.all()[::-1]
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data)
            else:
                Response(status=status.HTTP_403_FORBIDDEN)

            orders = Order.objects.filter(client_id=user.id)[::-1]
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

    def post(self, request):
        user = request.user
        request.data['client'] = user.id

        items = request.data.get('items', [])

        if len(items) < 1:
            return Response({'detail': 'Cant create order without products'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order_items = self.collect_orderItems(items)
            order = serializer.save()
            order.items.set(order_items)

            cart = Cart.objects.get(pk=user.id)
            cart.items.all().delete()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):    
        order = self.get_object(pk)

        if not order:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        user = request.user
        try:
            order = self.get_object(pk=pk)
            order.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_202_ACCEPTED)
