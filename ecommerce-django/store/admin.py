from django.contrib import admin
from django.contrib.auth.models import Group    

from .models import Category, Product, Order, OrderItem

# Remove Groups from admin
admin.site.unregister(Group)                    


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
