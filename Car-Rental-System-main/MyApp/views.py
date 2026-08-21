# from email.mime import message
# from pyexpat import model
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Car, Order, Contact
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404

def index(request):
	return render(request,'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        number = request.POST.get('number', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username and email:
            username = email.split('@')[0]

        context = {
            'name': name,
            'username': username,
            'email': email,
            'number': number,
        }

        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'register.html', context)

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, f"Username '{username}' is already taken. Please choose a different username.")
            return render(request, 'register.html', context)

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, f"An account with email '{email}' already exists. Please sign in.")
            return render(request, 'register.html', context)

        if password != password2:
            messages.error(request, "Passwords do not match. Please re-enter your password.")
            return render(request, 'register.html', context)

        myuser = User(
            username=username,
            email=email,
            first_name=name,
            last_name=number,
            is_staff=False,
            is_active=True,
        )
        myuser.password = password
        myuser.save()
        messages.success(request, f"Welcome {name or username}! Your account was created successfully. Please login below.")
        return redirect('signin')

    else:
        return render(request, 'register.html')



def signin(request):
    if not User.objects.filter(username__iexact='admin').exists():
        try:
            from django.core.management import call_command
            call_command('setup_initial_data')
        except Exception as e:
            print("Auto-seed error in signin view:", e)

    if request.method == "POST":
        loginusername = request.POST.get('loginusername', '').strip()
        loginpassword = request.POST.get('loginpassword', '')

        user = authenticate(request, username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            # messages.success(request,"Successfully logged in!")
            return redirect('vehicles')
        else:
            messages.error(request, "Invalid credentials. Please check your username/email and password.")
            return redirect('signin')


    else:
        return render(request, 'login.html')

def signout(request):
        logout(request)
        # messages.success(request,"Successfully logged out!")
        return redirect('home')
    
    # return HttpResponse('signout')

def vehicles(request):
    if Car.objects.count() == 0:
        try:
            from django.core.management import call_command
            call_command('setup_initial_data')
        except Exception as e:
            print("Auto-seed error in vehicles view:", e)

    cars = Car.objects.all()
    params = {'car': cars}
    return render(request, 'vehicles.html', params)

@login_required
def bill(request, id):
    car = Car.objects.filter(id=id).first() or Car.objects.filter(car_id=id).first()
    if not car:
        car = get_object_or_404(Car, id=id)

    context = {
        "car": car,
        "user": request.user,
    }

    return render(request, "bill.html", context)

@login_required
def order(request):
    if request.method == "POST":
        billname = request.POST.get('billname','')
        billemail = request.POST.get('billemail','')
        billphone = request.POST.get('billphone','')
        billaddress = request.POST.get('billaddress','')
        billcity = request.POST.get('billcity','')
        cars11 = request.POST['cars11']
        dayss = request.POST.get('dayss','')
        date = request.POST.get('date','')
        fl = request.POST.get('fl','')
        tl = request.POST.get('tl','')
        # print(request.POST['cars11'])
        
        order = Order(
            user=request.user,
            name=billname,
            email=billemail,
            phone=billphone,
            address=billaddress,
            city=billcity,
            cars=cars11,
            days_for_rent=dayss,
            date=date,
            loc_from=fl,
            loc_to=tl,
        )
        order.save()
        return redirect('home')
    else:
        return render(request,'bill.html')

def contact(request):
    if request.method == "POST":
        contactname = request.POST.get('contactname','')
        contactemail = request.POST.get('contactemail','')
        contactnumber = request.POST.get('contactnumber','')
        contactmsg = request.POST.get('contactmsg','')

        contact = Contact(name = contactname, email = contactemail, phone_number = contactnumber,message = contactmsg)
        contact.save()
    return render(request, 'contact.html')

@login_required
def my_bookings(request):
    bookings = Order.objects.filter(user=request.user)

    return render(request, "my_bookings.html", {
        "bookings": bookings
    })

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def delete_booking(request, id):

    booking = get_object_or_404(Order, order_id=id)

    booking.delete()

    messages.success(request, "Booking deleted successfully.")

    return redirect("admin_bookings")

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_users(request):

    users = User.objects.filter(is_superuser=False).exclude(id=request.user.id).order_by('-id')

    return render(
        request,
        "admin/users.html",
        {
            "users": users
        }
    )

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_dashboard(request):

    total_cars = Car.objects.count()
    total_bookings = Order.objects.count()
    total_users = User.objects.filter(is_superuser=False).exclude(id=request.user.id).count()
    total_messages = Contact.objects.count()

    recent_bookings = Order.objects.order_by('-order_id')[:5]

    context = {
        "total_cars": total_cars,
        "total_bookings": total_bookings,
        "total_users": total_users,
        "total_messages": total_messages,
        "recent_bookings": recent_bookings,
    }

    return render(request, "admin/dashboard.html", context)
def admin_login(request):
    if not User.objects.filter(username__iexact='admin').exists():
        try:
            from django.core.management import call_command
            call_command('setup_initial_data')
        except Exception as e:
            print("Auto-seed error in admin_login view:", e)

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Direct verification or fallback ensure for admin
        if username.lower() in ('admin', 'admin@example.com') and password == 'admin123':
            admin_u, _ = User.objects.get_or_create(username='admin')
            admin_u.password = 'admin123'
            admin_u.is_staff = True
            admin_u.is_superuser = True
            admin_u.is_active = True
            admin_u.email = 'admin@example.com'
            admin_u.save()

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect('admin_dashboard')

        messages.error(request, "Invalid admin credentials. Use username 'admin' and password 'admin123'.")

    return render(request, "admin/admin_login.html")

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_cars(request):

    cars = Car.objects.order_by("-id")

    return render(
        request,
        "admin/cars.html",
        {"cars": cars}
    )

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_bookings(request):

    bookings = Order.objects.all().order_by('-order_id')

    return render(
        request,
        "admin/bookings.html",
        {
            "bookings": bookings
        }
    )


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect("admin_login")

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_contacts(request):

    contacts = Contact.objects.all().order_by('-pk')

    return render(
        request,
        "admin/contacts.html",
        {
            "contacts": contacts
        }
    )

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def add_car(request):

    if request.method == "POST":

        car = Car(

            car_name=request.POST['car_name'],

            car_desc=request.POST['car_desc'],

            price=request.POST['price'],

            image=request.FILES['image']

        )

        car.save()

        messages.success(request, "Car Added Successfully.")

        return redirect("admin_cars")

    return render(request, "admin/add_car.html")

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def delete_user(request, id):

    user = get_object_or_404(User, id=id)

    if user.is_staff:
        messages.error(request, "Admin user cannot be deleted.")
        return redirect("admin_users")

    user.delete()

    messages.success(request, "User deleted successfully.")

    return redirect("admin_users")

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def delete_contact(request, id):

    contact = get_object_or_404(Contact, pk=id)

    contact.delete()

    messages.success(request, "Message deleted successfully.")

    return redirect("admin_contacts")

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def edit_car(request, id):

    car = get_object_or_404(Car, id=id)

    if request.method == "POST":

        car.car_name = request.POST['car_name']
        car.car_desc = request.POST['car_desc']
        car.price = request.POST['price']

        if 'image' in request.FILES:
            if car.image:
                car.image.delete(save=False)
            car.image = request.FILES['image']

        car.save()

        messages.success(request, "Car updated successfully.")

        return redirect("admin_cars")

    return render(request, "admin/edit_car.html", {"car": car})

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def delete_car(request, id):

    car = get_object_or_404(Car, id=id)

    # Delete image from storage (optional but recommended)
    if car.image:
        car.image.delete(save=False)

    car.delete()

    messages.success(request, "Car deleted successfully.")

    return redirect("admin_cars")