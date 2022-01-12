from rest_framework import serializers
from accounts.models import Customer
from .models import Food,FoodCategory,Meal,Branch

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['email']
        
class FoodSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"

class FoodCategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = "__all__"

class MealCategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"

class MealCategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"

class RestaurantBranchSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"