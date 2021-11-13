from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
def Registration(request):
    return render(request, "Registration/Registration.html")

@login_required
def Department(request):
    return render(request, "Manager/Department.html")

@login_required
def Total(request):
    return render(request, "Manager/Total.html")

def Register(request):
    return render(request, "layouts/register.html")

def ForgotPassword(request):
    return render(request, "layouts/forgot-password.html")
