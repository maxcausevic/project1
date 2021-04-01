from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.registration_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'first_name':
                messages.error(request, value, extra_tags='first_name')
            if key == 'last_name':
                messages.error(request, value, extra_tags='last_name')
            if key == 'reg_email':
                messages.error(request, value, extra_tags='reg_email')
            if key == 'reg_password':
                messages.error(request, value, extra_tags='reg_password')
            if key == 'confirm_pw':
                messages.error(request, value, extra_tags='confirm_pw')
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['reg_email'],
            password = request.POST['reg_password']
        )
        request.session['user_id'] = user.id
    return redirect('/shoppinglist')

def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'log_email':
                messages.error(request, value, extra_tags='log_email')
            if key == 'log_password':
                messages.error(request, value, extra_tags='log_password')
        return redirect('/')
    else:
        user_list = User.objects.filter(email=request.POST['log_email'])
        if len(user_list)==0:
            messages.error(request, 'We could not find a user with that email address.', extra_tags='log_email')
            return redirect('/')
        else:
            user=user_list[0]
            if request.POST['log_password'] == user.password:
                request.session['user_id'] = user.id
                return redirect('/shoppinglist')
            else:
                messages.error(request, 'Your password was incorrect.', extra_tags='log_password')
                return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            "all_products" : Product.objects.all()
        }
        return render(request, "success.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')

def submit_product(request):
    errors = Product.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shoppinglist')
    else:
        Product.objects.create(
            product_name = request.POST['product_name'],
            description = request.POST['description'],
            user = User.objects.get(id=request.session['user_id'])
        )
        return redirect('/add_product')

def add_product(request):
    return redirect('/shoppinglist')

def view_user_page(request, user_id):
    right_user = User.objects.get(id=user_id)
    user_products = Product.objects.filter(user=right_user)
    context = {
        'right_user':right_user,
        'user_products':user_products
    }
    return render(request, "userlist.html", context)

def see_account(request, user_id):
    right_user = User.objects.get(id=user_id)
    user_products = Product.objects.filter(user=right_user)
    context = {
        'right_user':right_user,
        'user_products':user_products
    }
    return render(request, "myaccount.html", context)

def edit_profile(request, user_id):
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'first_name':
                messages.error(request, value, extra_tags='first_name')
            if key == 'last_name':
                messages.error(request, value, extra_tags='last_name')
            if key == 'reg_email':
                messages.error(request, value, extra_tags='reg_email')
        return redirect(f'/myaccount/{user_id}')
    else:
        user = User.objects.get(id=user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['reg_email']
        user.save()
        return redirect(f'/myaccount/{user.id}') 

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('/shoppinglist')

def remove_product(request, product_id, user_id):
    user = User.objects.get(id=user_id)
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect(f'/user/{user.id}')