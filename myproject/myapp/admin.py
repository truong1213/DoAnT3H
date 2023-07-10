from django.contrib import admin
from .models import Product,Category,Profile,TokenReset,Cart,TokenRegister
# Register your models here.
# ******************************************** PRODUCT *********************************************
@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['id','name']
@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','category']
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id','user','name']
@admin.register(TokenReset)
class TokenReset(admin.ModelAdmin):
    list_display = ['user','token']
@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list_display = ['id','user','quantity','product']
@admin.register(TokenRegister)
class TokenRegister(admin.ModelAdmin):
    list_display = ['user','token']