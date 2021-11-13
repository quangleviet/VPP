from django.urls import path
from stationery import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.user_logout, name="logout"),
    path("Registration/", views.Registration, name="Registration"),
    path("Department/", views.Department, name="Department"),
    path("Total/", views.Total, name="Total"),
]