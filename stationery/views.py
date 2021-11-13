from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get ("password", "")
        user = authenticate(email=email, password=password)

        if user is None:
            my_message = (
            "Your email address or password is incorrect. Please login again!"
            )
            messages.error(request, my_message)
            
            return render(request, "layouts/login.html")
    
        login(request, user)
        return HttpResponseRedirect("dashboard/")

    return render(request, "layouts/login.html")
def dashboard(request):
    return render(request, "dashboard/index.html")