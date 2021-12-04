from django.urls import path
from stationery import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.user_logout, name="logout"),
    path("Registration/", views.Registration, name="Registration"),
    path("Department/", views.Department, name="Department"),
    path("Total/", views.Total, name="Total"),
    path("Register/", views.Register, name="Register"),
    path("ForgotPassword/", views.ForgotPassword, name="ForgotPassword"),
    path("CreateRegister/", views.Create_register, name="CreateRegister"),
    path("CreateStationery/", views.Create_stationery, name="CreateStationery"),
    path("RegistrationDetail/<int:regist_id>", views.Registration_detail, name="RegistrationDetail"),
    path("Registration/delete-regis/<int:pk>", views.delete_registration, name="delete_registration"),
    path("Registration/edit-regis/<int:pk>", views.edit_registration, name="edit_registration"),
]