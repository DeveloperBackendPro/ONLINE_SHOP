from home.models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['total_price']
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['name','phone','messages',]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['product','name','phone','rate','text']


class NewsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = News_comment
        fields = ['news','name','phone','rate','comment',]

class ShopCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopcart
        fields = ['client','product','color','quantity',]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['client','product','color','quantity','first_name','last_name',
                  'phone','country','city','address','zip_code','order_note','total_price',]