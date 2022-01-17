from django.contrib import admin
from .models import *

admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(FoodCategory)
admin.site.register(Menu)
admin.site.register(Branch)
admin.site.register(OrderItem)
admin.site.register(Food)
admin.site.register(Order)


# @admin.register(Branch)
# class CustomRestaurantBranch(admin.ModelAdmin):
#     model = Branch
#     list_display = ['name','address','status',]
#     list_editable = ['status',]
#     empty_value_display = 'is null'
#     list_filter = ['name','address','status',]
#     list_per_page = 4
#     search_fields = ['name','address','status',]

# @admin.register(OrderItem)
# class CustomMenu(admin.ModelAdmin):
#     model = OrderItem
#     list_display = ['number',]
#     empty_value_display = 'is null'
#     list_per_page = 4
#     search_fields = ['number',]
#     fieldsets = (
#             (None, {
#                 "fields": (
#                     'order','menu','number',
#                 ),
#             }),
#         )

# @admin.register(Food)
# class CustomFood(admin.ModelAdmin):
#     model = Food
#     list_display = ['food_name','food_image','food_description',]
#     list_editable = ['food_description',]
#     empty_value_display = 'is null'
#     list_filter = ['food_name',]
#     list_per_page = 4
#     search_fields = ['food_name',]
#     fieldsets = (
#             (None, {
#                 "fields": (
#                     'food_name','food_image','food_category_id',
#                 ),
#             }),
#             ('personal info', {
#                 "description": 'This is food information :)',
#                 "classes": ('collapse',),
#                 "fields": (
#                     'food_description',
#                 ),
#                 }
#             ),
#         )

# @admin.register(Order)
# class CustomOrder(admin.ModelAdmin):
#     model = Order
#     list_display = ['delivery_time','customer_status',]
#     list_editable = ['customer_status',]
#     empty_value_display = 'is null'
#     list_filter = ['customer_status',]
#     list_per_page = 4
#     search_fields = ['delivery_time','customer_status',]
#     fieldsets = (
#             (None, {
#                 "fields": (
#                     'order_item','total_price','customer','address','branch','customer_status',
#                 ),
#             }),
#         )