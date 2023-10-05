from rest_framework import serializers
from voidcms.models import Order, OrderItem, OrderProduct
from voidcms.drf.serializers.productSerializer import ProductSerializer

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_products(self, instance):
        products_data = instance.items.all().select_related('product')
        return [
            {
                "id": item.id,
                "count": item.count,
                "complectations": item.complectations,
                "product": OrderProductSerializer(item.product).data
            }
            for item in products_data
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = self.get_products(instance)
        return representation
