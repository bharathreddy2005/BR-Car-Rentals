from django.urls import path
from MyApp import views

urlpatterns = [
    path("", views.index, name="home"),
    path("home", views.index, name="home"),
    path("about", views.about, name="about"),

    path("vehicles", views.vehicles, name="vehicles"),

    path("register", views.register, name="register"),
    path("signup", views.register, name="signup"),

    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),

    path("bill/<int:id>/", views.bill, name="bill"),
    path("order", views.order, name="order"),

    path("contact", views.contact, name="contact"),
    path("my-bookings", views.my_bookings, name="my_bookings"),

    # Custom Admin
    path("dashboard/login/", views.admin_login, name="admin_login"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("dashboard/cars/", views.admin_cars, name="admin_cars"),
    path("dashboard/cars/add/", views.add_car, name="add_car"),
    path("dashboard/cars/edit/<int:id>/", views.edit_car, name="edit_car"),
    path("dashboard/cars/delete/<int:id>/", views.delete_car, name="delete_car"),

    path("dashboard/bookings/", views.admin_bookings, name="admin_bookings"),
    path("dashboard/bookings/delete/<int:id>/", views.delete_booking, name="delete_booking"),

    path("dashboard/users/", views.admin_users, name="admin_users"),
    path("dashboard/users/delete/<int:id>/", views.delete_user, name="delete_user"),

    path("dashboard/contacts/", views.admin_contacts, name="admin_contacts"),
    path("dashboard/contacts/delete/<int:id>/", views.delete_contact, name="delete_contact"),

    path("dashboard/logout/", views.admin_logout, name="admin_logout"),
]