from django.contrib import admin
from .models import User, TypeOfGoods, Product, Order, AdditionProduct, HistoryOrders, OrderResponse

admin.site.register(TypeOfGoods)
admin.site.register(OrderResponse)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(AdditionProduct)
admin.site.register(HistoryOrders)
admin.site.register(User)
