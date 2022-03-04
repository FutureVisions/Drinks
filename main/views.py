from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def home(request):
    return render(request, "log_reg.html")

def home_create(request):
    errors = User.objects.basic_validator(request.POST)
    user= User.objects.filter(email=request.POST['email'])
    if user:
        messages.error(request, "Email is already taken!")
        return redirect('/')
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=pw_hash)
        request.session['log_user_id'] = new_user.id
    return redirect('/dashboard')

def log_user(request):
    user= User.objects.filter(email=request.POST['email'])
    if user:
        logged_user= user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['log_user_id'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid Email or Password!', extra_tags='invalid')
            return redirect('/')
    messages.error(request, "Email does not exist")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    print('Dashboard')
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'all_drinks': Drink.objects.all()
    }
    return render(request, 'dashboard.html', context)

def profile(request, user_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    context = {
        "user_id": User.objects.get(id=request.session['log_user_id']),
        "all_drinks": Drink.objects.all(),
        "account_user": User.objects.get(id=user_id),
    }
    return render(request, "profile.html", context)

def add_drink(request):
    if "log_user_id" not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['log_user_id'])
    new_drink= Drink.objects.create(name=request.POST['name'], price=request.POST['price'], desc=request.POST['desc'], image=request.FILES['image'], content_creator = current_user)
    return redirect('/dashboard')

def update_drinks(request, drink_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    context = {
        "all_drinks": Drink.objects.all(),
        "this_drink": Drink.objects.get(id=drink_id)
    }
    return render(request, 'update.html', context)

def update(request, drink_id):
    drink_to_update= Drink.objects.get(id=drink_id)
    drink_to_update.name= request.POST['name']
    drink_to_update.price= request.POST['price']
    drink_to_update.desc= request.POST['desc']
    drink_to_update.image= request.FILES['image']
    drink_to_update.save()
    return redirect('/dashboard')

def delete(request, drink_id):
    drink_delete= Drink.objects.get(id=drink_id)
    drink_delete.delete()
    return redirect('/dashboard')

def cart(request):
    if "log_user_id" not in request.session:
        return redirect('/')
    if 'cart' not in request.session:
        request.session['cart'] = []
    drink_list = []
    total_amount= 0
    for item in request.session['cart']:
        drink = Drink.objects.get(id=item)
        drink_list.append(drink)
        total_amount = total_amount + drink.price
    context = {
        "total_amount": total_amount,
        "user_id": User.objects.get(id=request.session['log_user_id']),
        "all_drinks": Drink.objects.all(),
        "drink_list": drink_list
    }
    return render(request, "cart.html", context)

def add_cart(request):
    if 'cart' not in request.session:
        cart = []
    else:
        cart = request.session['cart']
    cart.append(request.POST['drink_id'])
    request.session['cart'] = cart
    context = {
        "user_id": User.objects.get(id=request.session['log_user_id']),
        "all_drinks": Drink.objects.all(),
        "drink_list": request.session['cart']
    }
    return redirect('/cart')

def checkout(request):
    if 'cart' not in request.session:
        return redirect('/')
    new_order = Order.objects.create(
        order_customer_id = request.session['log_user_id']
    )
    for drink_id in request.session['cart']:
        drink = Drink.objects.get(id=drink_id)
        amount = drink.price * 1
        unit_price = drink.price
        detail1= OrderDetail.objects.create( 
            order_number = new_order,
            quantity = 1,
            unit_price = unit_price,
            amount = amount
        )
        detail1.drinks.add(drink)
    request.session['order_id'] = new_order.id
    request.session['cart'] = []
    return redirect('/success')

def success(request):
    if 'log_user_id' not in request.session:
        return redirect('/')
    
    order = Order.objects.get(id=request.session['order_id'])
    sum = 0
    for detail in order.order_details.all():
        sum += detail.amount
    context = {
        'sum': sum,
        'customer': User.objects.get(id=request.session['log_user_id']),
        'order': order,
        'order_details': OrderDetail.objects.all()

    }
    return render(request, 'success.html', context)