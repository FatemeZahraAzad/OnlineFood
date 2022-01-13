from django.urls.base import reverse
from django.views.generic.base import TemplateView
from accounts.models import Address,CustomerAddress, Manager
from .models import *
from .serializers import *
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy
from django.db.models import Sum
from .serializers import *
from .decorator import superuser_required, is_staff_required, customer_required
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
"""
_________________________________________________________Foods_________________________________________________________

"""

def foodView(req):
    foods = Food.objects.all()
    return render(req, "foods.html", {"foods": foods})

def show_foods(req):
    foods = Food.objects.all()
    menus = Menu.objects.all()
    most_seller_restaurant = Branch.objects.filter(branch_menus__orderitems__order__customer_status = "order_confirmed").annotate(sum_totalprice=Sum("branch_menus__orderitems__order__total_price")).order_by("-sum_totalprice")[:10]
    most_seller_foods = Food.objects.all().filter(food_menu__orderitems__order__customer_status = "order_confirmed").annotate(sum_number=Sum("food_menu__orderitems__number")).order_by("-sum_number")[:10]
    return render(req, "home.html", {"foods": foods,"menus":menus,'most_seller_foods':most_seller_foods,'most_seller_restaurant':most_seller_restaurant})

@superuser_required()
class FoodCreate(CreateView):
    model = Food
    template_name = "websitemanager.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

class FoodUpdate(UpdateView):
    model = Food
    template_name = "update_food.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

class FoodDelete(DeleteView):
    model = Food
    template_name = "delete_food.html"
    success_url = reverse_lazy('foods')
    fields = "__all__"

class PostFoodCategoryCreate(CreateView):
    model = FoodCategory
    template_name = "food_category_form.html"
    success_url = reverse_lazy('add_food')
    fields = "__all__"   

"""
_________________________________________________________Product_________________________________________________________

"""

def food(request,pk):  
    menus = Menu.objects.get(id = pk)
    food = Food.objects.get(food_menu__id = pk)
    if request.method == 'POST':
        try:
            customer = request.user.device
            if Customer.objects.get(username=request.user.device):
                c_customer = Customer.objects.get(username=request.user.device)
                c_customer.delete()
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(username=device,email=device+"@gmail.com",device=device)
        if Order.objects.filter(customer=customer).filter(customer_status="ordered") and Menu.objects.filter(orderitems__order__customer_status="ordered").filter(orderitems__order__customer=customer):
            if (Menu.objects.filter(id = pk).values_list("branch__name").last())[0] == Menu.objects.filter(orderitems__order__customer_status="ordered").filter(orderitems__order__customer=customer).values_list("branch__name").first()[0]:
                if ((Menu.objects.filter(id = pk).values_list('menu_number').last())[0]) >= int(request.POST['number']):  #موجودی انبار
                    order, created = Order.objects.get_or_create(customer=customer, customer_status='ordered')
                    orderItem, created = OrderItem.objects.get_or_create(order=order, menu=menus)
                    orderItem.number =request.POST['number']
                    orderItem.save()
                    return redirect('add_to_cart')
                else:
                    context = {'menus':menus, "food":food ,'msg':"not enough foods"}
                    return render(request, 'order_detail.html', context)
            else:
                return render(request, 'order_detail.html', {'menus':menus, "food":food ,'msg':"you should remove current orders."})
        else:
            if (Menu.objects.all().filter(id = pk).values_list('menu_number').last())[0]>= int(request.POST['number']):
                order, created = Order.objects.get_or_create(customer=customer, customer_status='ordered')
                orderItem, created = OrderItem.objects.get_or_create(order=order, menu=menus)
                orderItem.number =request.POST['number']
                orderItem.save()
                return redirect('add_to_cart')
            else:
                return render(request, 'order_detail.html', {'menus':menus, "food":food ,'msg':"not enough!"})
    return render(request, 'order_detail.html', {'menus':menus, "food":food })

"""
_________________________________________________________Cart_________________________________________________________

"""

def cart(request):
    if request.method =="POST":
        if request.user:
            orderitems = OrderItem.objects.filter(order__customer_status="ordered")
            total_price = sum([item.get_total for item in orderitems])
            device = request.COOKIES['device']
            branch_id = Menu.objects.filter(orderitems__order__customer_status="ordered").filter(orderitems__order__customer__device=device).values_list("branch__id").first()[0]
            branch_order = Order.objects.get(customer_status = "ordered")
            branch_address = request.POST['cart_address']
            customer_address = CustomerAddress.objects.get(id=branch_address)
            branch = Branch.objects.get(id = branch_id)
            branch_order.branch = branch
            branch_order.total_price = total_price
            branch_order.customer_status = "order_confirmed"
            branch_order.address = customer_address
            branch_order.save()
            return render(request,"cart.html",{'msg':"no orderitems available!"})
        else:
            return reverse('add_to_cart')
    try:
        customer = request.user.device
        if Customer.objects.get(username=request.user.device):
            c_customer = Customer.objects.get(username=request.user.device)
            c_customer.delete()
    except:
        device = request.COOKIES['device']
        customer = device
    customer_address = CustomerAddress.objects.all()
    orderitems=OrderItem.objects.filter(Q(order__customer__device=customer) & Q(order__customer_status="ordered"))
    food = Food.objects.filter(food_menu__orderitems__order__customer__device=customer)
    orders = Order.objects.filter(customer__device=customer).filter(customer_status = "ordered")
    return render(request, 'cart.html', {'orders':orders,"orderitems": orderitems,"food":food,"customer_address":customer_address})

class OrderItemDeleteView(DeleteView):
    model = OrderItem
    template_name = "delete_food.html"
    success_url = reverse_lazy("add_to_cart")
    fields = "__all__"


#____________________________________________________phase 3_______________________________________________________________

"""
_________________________________________________________Restuarent Panel_________________________________________________________

"""
@is_staff_required()
class BranchUpdate(UpdateView):
    model = Branch
    template_name = "restaurant/branch_address_edit.html"
    success_url = reverse_lazy('restaurant_panel')
    fields= "__all__"

@is_staff_required()
class MenuCreate(CreateView):
    model = Menu
    template_name = "restaurant/create_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = ["food","menu_number","price"]

    def post(self, request, *args, **kwargs):
        branch = Branch.objects.get(manager__username = self.request.user.username)
        food = request.POST["food"]
        foods = Food.objects.get(id = food)
        price = request.POST["price"]
        menu_number = request.POST["menu_number"]
        form = self.get_form()
        if form.is_valid():
            new = Menu.objects.create(branch = branch,food = foods , price = price ,menu_number = menu_number )
            return redirect("restaurant_panel")
        else:
            return self.form_invalid(form)
    
@is_staff_required()
class ManagerMenus(TemplateView):
  template_name = "restaurant/branch.html"
  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    context["manager_menus"] = Menu.objects.filter(branch__manager__username = self.request.user.username)
    context["branchs"] = Branch.objects.get(manager__username=self.request.user.username)
    context["manager"] = Manager.objects.get(username=self.request.user.username)
    context["orders"] = Order.objects.filter(branch__manager__username=self.request.user.username).exclude(customer_status = "ordered")
    return context

@is_staff_required()
class MenuUpdate(UpdateView):
    model = Menu
    template_name = "restaurant/edit_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = ["menu_number","price"]

@is_staff_required()
class MenuDelete(DeleteView):
    model = Menu
    template_name = "restaurant/delete_menu.html"
    success_url = reverse_lazy('restaurant_panel')
    fields = "__all__"

class BranchList(ListView):
    contecxt_object_name = "branchs"
    model = Branch
    template_name = "restaurant/restaurant.html"


class BranchDetail(DetailView):
    contecxt_object_name = "branch_detail"
    queryset = Branch.objects.all()
    model = Branch
    template_name = "restaurant/branch_detail.html"

"""
_________________________________________________________Customer Panel_________________________________________________________

"""

@customer_required()
class CustomerOrders(TemplateView):
    template_name = "customer/customer_panel.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = Address.objects.filter(customer_address__customer_id__username=self.request.user.username)
        context['orders'] = Order.objects.filter(customer__username=self.request.user.username)
        return context
        
"""
_________________________________________________________Search_________________________________________________________

"""
# def search_result(request):
#     results=[]
#     if request.method == 'GET':
#         data = request.GET.get('search')
#         results = Menu.objects.filter(Q(food__food_name__icontains=data) | Q(branch__name__icontains=data))  
#         print(results) 
#         print("__________________________________________________")
#         print(data)
#     return render(request,"search/search.html",{'data':data,'results':results})

def search_result(req):
    """
        all users are able to search food and restaurant's name
    """
    results=[]
    if req.method == 'GET':
        query = req.GET.get('search')
        if query == '':
            query = 'None'
        results = Menu.objects.filter(Q(food__food_name__icontains= query)| Q(branch__name__icontains=query))
    context ={'query': query, 'results': results}
    print(results)
    return render(req, 'search/search.html', context)