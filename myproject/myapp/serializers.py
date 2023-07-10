from rest_framework import serializers
from . models import Product,Category,Profile,TokenReset,TokenRegister,Cart
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
class TokenResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenReset
        fields = '__all__'
class CartSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title')
    product_price = serializers.FloatField(source='product.discounted_price')
    product_img = serializers.ImageField(source = 'product.product_image')
    class Meta:
        model = Cart
        fields = '__all__'
class TokenRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenRegister
        fields = '__all__'
        
