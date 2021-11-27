from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Registrations, Room, Registrations, Stationery, Unit, Regist_detail


# Create your views here.
def user_login(request, method="POST"):
    if request.method == 'POST':
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(email=email, password=password)

        if user is None:
            my_message = (
                "Your email address or password is incorrect. Please login again"
            )
            messages.error(request, my_message)
            return render(request, "layouts/login.html")
        login(request, user)
        return HttpResponseRedirect("dashboard/")
    return render(request, "layouts/login.html")

@login_required
def dashboard(request):
    return render(request, "dashboard/index.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def Registration(request, method="GET"):
    units = Unit.objects.all
    stationerys = Stationery.objects.all
    return render(request, "Registration/Registration.html", {"units" : units, "stationerys" :stationerys})

@login_required
def Department(request, method="GET"):
    registrations = Registrations.objects.all
    return render(request, "Manager/Department.html", {"registrations": registrations})

@login_required
def Create_register(request, method="GET"):
    rooms = Room.objects.all
    registrations = Registrations.objects.all
    stationerys = Stationery.objects.all

    if request.method == "POST":
        data = request.POST
        list_stationery = data.getlist("stationery[]", [])
        list_amount = data.getlist("amount[]", [])
        list_unit = data.getlist("unit[]", [])
        if len(list_stationery) and len(list_amount) and len(list_unit):
            list_stationery_amount_unit = []
            i = 0

            for ind in range(0, len(list_stationery)):
                list_stationery_amount_unit.append(
                    __new_stationery_amount_unit(
                        stationery_id=int(list_stationery[ind]),
                        amount_id=int(list_amount[ind]),
                        unit_id=int(list_unit[ind]),
                    )
                )
            Stationery.objects.bulk_create(list_stationery_amount_unit)

            return redirect("Registration")
    return render(request, "Registration/create_register.html", {"rooms": rooms, "registrations" : registrations, "stationerys": stationerys})


def __new_stationery_amount_unit(stationery_id, amount_id, unit_id):
    stationery_amount_unit = Stationery()
    stationery_amount_unit.stationery_id = stationery_id,
    stationery_amount_unit.amount_id = amount_id,
    stationery_amount_unit.unit_id = unit_id,

    return stationery_amount_unit


def Register(request):
    return render(request, "layouts/register.html")

def ForgotPassword(request):
    return render(request, "layouts/forgot-password.html")

@login_required
def Total(request, method="GET"):
    units = Unit.objects.all
    stationerys = Stationery.objects.all
    return render(request, "Manager/Total.html", {"units" : units, "stationerys" :stationerys})



