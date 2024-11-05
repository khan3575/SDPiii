from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html",{})

def login(request):
    return render(request,"login.html")

def authView(request):
    if request.method== "POST":
        form= UserChangeForm(request.POST or none)
        if form.is_valid():
            form.save()
    else:
        form=UserChangeForm()

    
    return render(request, "registration/signup.html", { "form": form})