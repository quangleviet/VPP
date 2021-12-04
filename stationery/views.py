from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import Context, Template

from .models import Registrations, Room, Registrations, Stationery, Unit, RegistDetail


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
    registrations = Registrations.objects.all()
    return render(request, "Registration/Registration.html", {"registrations" :registrations})

@login_required
def Department(request, method="GET"):
    registrations = Registrations.objects.all
    quarters = Registrations.QUARTER
    return render(request, "Manager/Department.html", {"registrations": registrations, "quarters": quarters})

@login_required
def Create_register(request, method="GET"):
    rooms = Room.objects.all
    registrations = Registrations.objects.all
    stationerys = Stationery.objects.all
    quarters = Registrations.QUARTER

    if request.method == "POST":
        data = request.POST
        list_stationery = data.getlist("stationery[]", [])
        list_amount = data.getlist("amount[]", [])


        room = int(data.get("room", ""))
        quarter = data.get("quarter", "")
        comment = data.get("comment", "")
        registration = Registrations(room_id=room, quarter=quarter, comment=comment)
        registration.save()


        if len(list_stationery) and len(list_amount):
            list_stationery_amount_unit = []

            for ind in range(0, len(list_stationery)):
                list_stationery_amount_unit.append(
                    __new_stationery_amount_unit(
                        stationery_id=int(list_stationery[ind]),
                        amount=int(list_amount[ind]),
                        regist=registration
                    )
                )
            
            RegistDetail.objects.bulk_create(list_stationery_amount_unit)

            return redirect("Registration")
    return render(request, "Registration/create_register.html",
        {"rooms": rooms, "registrations" : registrations, "stationerys": stationerys, "quarters": quarters})


def __new_stationery_amount_unit(stationery_id, amount, regist):
    regis_detail = RegistDetail()
    regis_detail.stationery_id = stationery_id
    regis_detail.amount = amount
    regis_detail.registration = regist
    print("===========")
    print(regis_detail.__dict__)

    return regis_detail


def Register(request):
    return render(request, "layouts/register.html")

def ForgotPassword(request):
    return render(request, "layouts/forgot-password.html")

@login_required
def Total(request, method="GET"):
    units = Unit.objects.all
    stationerys = Stationery.objects.all
    return render(request, "Manager/Total.html", {"units" : units, "stationerys" :stationerys})

@login_required
def Registration_detail(request, regist_id):
    regisdetails = RegistDetail.objects.filter(registration_id=regist_id)
    stationerys = Stationery.objects.all
    return render(request, "Registration/Registration_detail.html", {"regisdetails" : regisdetails, "stationerys" :stationerys})

@login_required
def Create_stationery(request):
    if request.method == "GET":
        stationerys = Stationery.objects.all()
        return render(request, "Manager/create_stationery.html", {"stationerys" : stationerys})
    elif request.method == "POST":
            try:
                data = request.POST
                name = data.get("name", "")
                unit = data.get("unit", "")
                stationery = Stationery(name=name, unit=unit)
                stationery.save()
                messages.success(request, "Create Stationery successful")
            except:
                messages.error(request, "Create Stationery failed")
                return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return HttpResponseRedirect(reverse("CreateStationery"))

