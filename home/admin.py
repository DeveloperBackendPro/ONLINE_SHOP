from home.models import *
from django.contrib import admin
from django.utils.html import format_html

class InformationAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone', 'email']
    exclude = ('about_us',)

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('code','title')

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','total_count',]
    exclude = ('code','title','description_full',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_full_name', 'client_total_price']

class CodeAdmin(admin.ModelAdmin):
    list_display = ['client_full_name', 'number']

class Product_ElementsAdmin(admin.ModelAdmin):
    list_display = ['product','color', 'color_all']

    def color_all(self, obj):
        return format_html('<div style="width: 12px; height: 12px; background-color:{};"></div>', obj.color, obj.color)
    color_all.short_description = 'Цвет'
class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['display_color','product','client_full_name','calculate_total_price','quantity', ]
    def display_color(self, obj):
        return format_html('<div style="width: 20px; height: 20px; background-color:{};"></div>', obj.color, obj.color)
    display_color.short_description = 'Цвет'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['display_color', 'product','client_full_name','phone','quantity','total_price']
    def display_color(self, obj):
        return format_html('<div style="width: 12px; height: 12px; background-color:{};"></div>', obj.color, obj.color)
    display_color.short_description = 'Цвет'

class FaqAdmin(admin.ModelAdmin):
    exclude = ('question','response',)

class NewsAdmin(admin.ModelAdmin):
    exclude = ('title','short_description','description',)

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','total_price',]



admin.site.register(Comment)
admin.site.register(ContactUs)
admin.site.register(News_comment)
admin.site.register(Faq, FaqAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Shopcart, ShopCartAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Product_Elements, Product_ElementsAdmin)
