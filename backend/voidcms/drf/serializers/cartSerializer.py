from rest_framework import serializers
from voidcms.models import Cart, CartItem
from voidcms.drf.serializers.productSerializer import ProductSerializer, ComplectationSerializer, ComplectationField


class CartItemSerializer(serializers.ModelSerializer):
    complectations = ComplectationSerializer(many=True, read_only=True)
    product = ProductSerializer()
    
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)


    class Meta:
        model = Cart
        fields = '__all__'
    

    def get_products(self, instance):
        products_data = instance.items.all().select_related('product')
        return [
            {
                "id": item.id,
                "count": item.count,
                "complectations": item.complectations,
                "product": ProductSerializer(item.product).data
            }
            for item in products_data
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = self.get_products(instance)
        return representation
