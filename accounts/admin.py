from django.contrib import admin
from .models import Product , Address , Cart , OrderPlaced

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['user','product','address','date','status']
    list_editable=['status']

@admin.register(Address)
class AddressModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state','pincode']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','slug','description','price','image','created','updated','category']
    list_editable=['price']
    prepopulated_fields={'slug':('title',)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['user','product','qty']
    list_editable=['qty']