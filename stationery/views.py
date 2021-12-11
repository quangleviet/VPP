from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import Context, Template
from django.forms.models import model_to_dict
from django.urls import reverse
import datetime

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
    statuses = Registrations.STATUS

    if request.method == "POST":
        data = request.POST
        print(data)
        list_stationery = data.getlist("stationery[]", [])
        list_amount = data.getlist("amount[]", [])
        room = int(data.get("room", ""))
        quarter = data.get("quarter", "")
        comment = data.get("comment", "")
        created_at = datetime.date.today()
        published_date = data.get("published_date", None)
        registration = Registrations(room_id=room, quarter=quarter, comment=comment, created_at=created_at, published_date=published_date)
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
        {"rooms": rooms, "registrations" : registrations, "stationerys": stationerys, "quarters": quarters, "statuses": statuses})


def __new_stationery_amount_unit(stationery_id, amount, regist):
    regis_detail = RegistDetail()
    regis_detail.stationery_id = stationery_id
    regis_detail.amount = amount
    regis_detail.registration = regist
    return regis_detail

# def edit_registration(request, pk):
# regis = get_object_or_404(Registration, pk=pk)

#     if request.method == "POST":
#         form = CreateRegisForm(request.POST or None)
#         if form.is_valid():
#             # book = Book()

#             regis.name = form.cleaned_data["name"]
#             regis.description = form.cleaned_data["description"]
#             regis.author = form.cleaned_data["author"]
#             regis.published_date = form.cleaned_data["published_date"]


#             regis.save()  # book.refresh_from_db() // book.update(name='', description='', ...)

#             messages.success(request, "Create book successful")
#             return redirect("list_books")
#     else:
#         form = CreateRegisForm(model_to_dict(book))

#     context = {"form": form, "book": book}
# return render(request, "books/edit_book_f.html", context=context)

def delete_registration(request, pk):
    regis = get_object_or_404(Registrations, pk=pk)
    regisdetails = RegistDetail.objects.filter(registration_id=pk)
    regisdetails.delete()
    regis.delete()

    return redirect("Registration")

def edit_registration(request, pk):
    regis = get_object_or_404(Registrations, pk=pk)
    regis_details = regis.registdetail_set.all()
    rooms = Room.objects.all
    stationerys = Stationery.objects.all
    quarters = Registrations.QUARTER

    if request.method == "POST":
        data = request.POST
        print(data)

        list_stationery = data.getlist("stationery[]", [])
        list_amount = data.getlist("amount[]", [])

        list_regis_detail_id = data.getlist("regis_detail_id[]", [])
        list_exist_stationery = data.getlist("exist_stationery[]", [])
        list_exist_amount = data.getlist("exist_amount[]", [])


        regis.room_id = int(data.get("room", ""))
        regis.quarter = data.get("quarter", "")
        regis.comment = data.get("comment", "")
        regis.save()

        if len(list_exist_stationery) and len(list_exist_amount) and len(list_regis_detail_id):
            list_stationeries = []

            for ind in range(0, len(list_exist_stationery)):
                list_stationeries.append(
                    __edit_stationery(
                        regis_detail_id=int(list_regis_detail_id[ind]),
                        stationery_id=int(list_exist_stationery[ind]),
                        amount=int(list_exist_amount[ind])
                    )
                )
            RegistDetail.objects.bulk_update(list_stationeries, fields=["stationery_id", "amount"])

        if len(list_stationery) and len(list_amount):
            list_stationery_amount_unit = []

            for ind in range(0, len(list_stationery)):
                list_stationery_amount_unit.append(
                    __new_stationery_amount_unit(
                        stationery_id=int(list_stationery[ind]),
                        amount=int(list_amount[ind]),
                        regist=regis
                    )
                )
            
            RegistDetail.objects.bulk_create(list_stationery_amount_unit)

        
        return redirect("Registration")
        # context = {"regis": model_to_dict(Registrations), "rooms": rooms, "stationerys": stationerys, "quarters": quarters}
    return render(request, "Registration/edit_registration.html",
        {"regis": model_to_dict(regis), "rooms": rooms,
        "stationerys": stationerys, "quarters": quarters, "regis_details": regis_details})

def __edit_stationery(regis_detail_id, stationery_id, amount):
    regis_detail = RegistDetail.objects.get(id=regis_detail_id)
    regis_detail.stationery_id = stationery_id
    regis_detail.amount = amount
    # regis_detail.save()
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
def Registration(request, method="GET"):
    rooms = Room.objects.all
    registrations = Registrations.objects.all()
    quarters = Registrations.QUARTER
    query_params = request.GET
    date_from = query_params.get("date_from", None)
    date_to = query_params.get("date_to", None)
    room=query_params.get("room", None)
    if date_from is not None:
        registrations = registrations.filter(created_at__gte=date_from)  # greater than equal

    if date_to is not None:
        registrations = registrations.filter(created_at__lte=date_to)

    if room is not None:
        registrations = registrations.filter(room=room)

    return render(request, "Registration/Registration.html",
        {"registrations" :registrations, "rooms" :rooms, "quarters":quarters, "queries":{"room_id": room or None}})

@login_required
def Registration_detail(request, regist_id):
    registrations = get_object_or_404(Registrations, id=regist_id) #Registrations.objects.get(id=regist_id)
    regisdetails = RegistDetail.objects.filter(registration_id=regist_id)
    stationerys = Stationery.objects.all   

    return render(request, "Registration/Registration_detail.html", {"registrations" : registrations, "regisdetails" : regisdetails, "stationerys" :stationerys})

def approve_regist(request, regist_id, method="POST"):
    registrations = get_object_or_404(Registrations, id=regist_id)
    # if request.method == "POST":
    action_data = request.POST
    print("==================")
    print(action_data)

    if action_data.get("status_approve", "") == '2':
        registrations.status = 2
        registrations.save()
    else:
        registrations.status = 3
        registrations.save()
    
    return redirect('Registration')


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

