from django.db import models
from django.core.validators import MinValueValidator
import jdatetime
from accounts.models import *


class Order(models.Model):
    customer = models.ForeignKey(Customer,related_name="customer_order",on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(CustomerAddress,on_delete=models.SET_NULL,related_name="orders",null=True)
    CUSTOMERSTATUS = [('ordered','ordered'),('order_confirmed','order_confirmed'),('is_sending','is_sending'),('delivered','delivered')]
    customer_status = models.CharField(choices=CUSTOMERSTATUS,default="-----",max_length=16)
    delivery_time = models.TimeField(auto_now_add=True)
    order_date = models.DateField(auto_now_add=True)
    branch = models.ForeignKey('Branch',on_delete=models.SET_NULL,null=True, blank=True,related_name="delivery")
    order_item = models.ManyToManyField('Menu', related_name="order")
    total_price = models.IntegerField(null=True)
        

    @property
    def get_cart_total(self):
        orderitems = OrderItem.objects.all().filter(order=self.id)
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = OrderItem.objects.all().filter(order=self.id)
        total = sum([item.number for item in orderitems])
        return total 

    @property 
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime= self.order_date)

    
    def __str__(self):
        return self.customer_status


class Food(models.Model):
    food_name = models.CharField(max_length=200,verbose_name="food_name")
    food_category_id = models.ForeignKey("FoodCategory",on_delete=models.CASCADE,related_name="menues")
    food_image = models.ImageField(upload_to = 'media/')
    food_description = models.TextField(max_length=1000,default="",verbose_name="food_description",null = True,blank=True)
    food_created_date = models.DateField(auto_now_add=True)
    meal = models.ManyToManyField('Meal',related_name="meal_menues")

    @property 
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime= self.food_created_date)

    def __str__(self):
        return self.food_name

class FoodCategory(models.Model):
    food_category_name = models.CharField(max_length=200,verbose_name="food_category_name")

    def __str__(self):
        return self.food_category_name

class Meal(models.Model):
    meal_category_name = models.CharField(max_length=200,verbose_name="meal_category_name")

    def __str__(self):
        return self.meal_category_name

class Menu(models.Model):
    food = models.ForeignKey(Food,related_name="food_menu",on_delete=models.SET_NULL,null=True)
    branch= models.ForeignKey('Branch', on_delete=models.CASCADE,related_name="branch_menus")
    menu_number = models.IntegerField(validators = [MinValueValidator(1)])
    price = models.IntegerField(validators = [MinValueValidator(20000)])

    def __str__(self):
        return self.food.food_name



class OrderItem(models.Model):   #middle table
    order = models.ForeignKey(Order,related_name="order_items",on_delete=models.SET_NULL,null=True)
    number = models.IntegerField(validators = [MinValueValidator(1)],null=True)
    menu = models.ForeignKey(Menu, related_name='orderitems', on_delete=models.SET_NULL,null=True)

    @property
    def get_total(self):
        foodname = str(Food.objects.all().filter(food_menu__orderitems__id=self.id).values_list('food_name')[0][0])
        #?????? ???????? ???? ?????? ?????? ?????????? ???????? ?????? ???? ????????????
        total = int(Menu.objects.all().filter(orderitems__order=self.order).filter(food__food_name=foodname).values_list("price")[0][0]) * self.number
        #?????? ???????? ????  ?????????? ?????????????? ???????? ???????? ?????????? ???????? ??????
        return total

    def __str__(self):
        return f"food number : {self.number}"

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=200,verbose_name="restaurant_name")

    def __str__(self):
        return self.restaurant_name


class Branch(models.Model):
    food_category = models.ForeignKey(FoodCategory,on_delete=models.CASCADE,related_name='branch')
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="restaurant_branchs")
    name = models.CharField(max_length=200,verbose_name="name")
    address = models.CharField(max_length=150)
    description = models.TextField(max_length=1000,default="",verbose_name="description",blank=True,null=True)
    created_date = models.DateField(auto_now_add=True)
    status = models.BooleanField('active',default=True)
    manager = models.OneToOneField(Manager,on_delete=models.CASCADE,related_name='branchs')
    is_main_branch = models.BooleanField(default=True)

    @property 
    def created_at_jalali(self):
        return jdatetime.datetime.fromgregorian(datetime= self.created_date)

    def __str__(self):
        return self.name

