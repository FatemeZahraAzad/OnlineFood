from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView, UpdateView
from orderonline.models import Order, Branch
from .forms import ManagerSignUpForm,CostumerSignUpForm
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

"""
_________________________________________________________Signup Manager_________________________________________________________

"""
def manager_signup(request):
	form = ManagerSignUpForm()
	if request.method == "POST":
		form = ManagerSignUpForm(request.POST)
		if form.is_valid() and request.POST["password"] and request.POST["password2"] and request.POST["password"] == request.POST["password2"]:
			form = form.save()
			return redirect("home")
		return render(request , "account/signup.html" , {"form":form,"msg":"something went wrong"})

	return render(request , "account/signup.html" , {"form":form})


class BranchManagerEdit(UpdateView):
	model = Branch
	template_name = "restaurant/branch_edit.html"
	success_url = reverse_lazy('restaurant_panel')
	fields = ["food_category","restaurant","name","address","description","status","is_main_branch"]

class ManagerEdit(UpdateView):
	model = Manager
	template_name = "account/manager_edit.html"
	success_url = reverse_lazy('restaurant_panel')
	fields = ["username","first_name","last_name"]

"""
_________________________________________________________Signup Customer_________________________________________________________

"""
def customer_signup(request):
	if request.method == "POST":
		form = CostumerSignUpForm(request.POST)
		
		if form.is_valid():
			form.save()
			customer = Customer.objects.get(username = request.POST["username"])
			address = Address.objects.create(state=request.POST["state"],city=request.POST["city"],street=request.POST["street"],pluque=request.POST["pluque"])
			cusromer_address = CustomerAddress.objects.create(customer_id = customer,address_id = address,is_main_address=True)
			
			return redirect('home')
	form = CostumerSignUpForm()
	return render(request,"account/customer_signup.html",{"form":form})

class CustomerEdit(UpdateView):
	model = Customer
	template_name = "account/customer_edit.html"
	success_url = reverse_lazy('customer_panel')
	fields = ["username","password","first_name","last_name"]

class CustomerSignOut(DeleteView):
	model = Customer
	template_name = "account/customer_signout.html"
	success_url = reverse_lazy('home')

"""
_________________________________________________________Address Customer_________________________________________________________

"""

def address_create(request):
	if request.method == "POST":
		state = request.POST['state']
		city = request.POST['city']
		street = request.POST['street']
		pluque = request.POST['pluque']
		is_main_address = request.POST["it_is"]

		device = request.COOKIES['device']
		customer = request.user
		customer , create = Customer.objects.get_or_create(email = customer)
		address  = Address.objects.create(state=state,city = city,street = street,pluque=int(pluque))
		if is_main_address == "True":

			edit, created = CustomerAddress.objects.filter(customer_id__email = customer).get_or_create(is_main_address =True)
			edit.is_main_address = False
			edit.save()
			
			
			customeraddress = CustomerAddress.objects.create(address_id = address,customer_id = customer,is_main_address=True)
		else:
			customeraddress = CustomerAddress.objects.create(customer_id = customer , address_id = address,is_main_address=False)
			return redirect('add_to_cart')
	return render(request,'choose_address.html')

@login_required
def delete_address(request,pk):
	if not request.user.is_staff:
		context = {}
		context["orders"] = Order.objects.filter(customer__username = request.user.username)
		context["address"] = Address.objects.filter(customer_address__customer_id__username=request.user.username)
		if CustomerAddress.objects.filter(address_id__id = pk).values_list("is_main_address")[0][0] == True:
			context["msg"] = "you cannot delete your last address!"
			return render(request,'customer/customer_panel.html',context)
		else:
			address = CustomerAddress.objects.get(address_id__id = pk)
			address.delete()
			context["msg"] = "address deleted successfully!"
			return render(request,'customer/customer_panel.html',context)
	else:
		return render(request,'customer/customer_panel.html',{"msg":"you are not manager!"})

@login_required
def change_main_address(request,pk):
	if not(request.user.is_staff ):
		context = {}
		context["orders"] = Order.objects.filter(customer__username = request.user.username)
		context["address"] = Address.objects.filter(customer_address__customer_id__username = request.user.username)
		if CustomerAddress.objects.filter(address_id__id= pk).values_list("is_main_address")[0][0] != True:
			customer_address = CustomerAddress.objects.filter(customer_id__username=request.user.username).get(is_main_address=True)
			customer_address.is_main_address = False
			customer_address.save()
			address = CustomerAddress.objects.get(address_id__id = pk)
			address.is_main_address = True
			address.save()
			context["msg"] = "chosen address changed to main address!"
		else:
			context["msg"] = "this is your default!"
			return render(request,"customer/customer_panel.html",context)
	else:
		return render(request,"customer/customer_panel.html",{"msg":"you are not a customer"})
"""
_________________________________________________________Login_________________________________________________________

"""
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {email}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="accounts/login.html", context={"login_form":form})