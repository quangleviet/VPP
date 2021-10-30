from django.urls import path

from stationery import views

urlpatterns = [
    path ("login/", views.login, name="login"),
    path ("dashboard/", views.dashboard, name="dashboard"),
]