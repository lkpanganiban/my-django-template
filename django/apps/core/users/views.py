from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm

# Create your views here.
def login_page(request):
    logout(request)
    errors = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, "pages/home.html")
        else:
            errors = "Invalid username and password combination!"
    return render(request, "pages/login.html",{"errors": errors})

def register_page(request):
    errors = None
    if request.method == 'POST':
        query_dict = request.POST.copy()
        query_dict["username"] = request.POST.get("email")
        form = RegistrationForm(query_dict)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.organization = form.cleaned_data.get('organization')
            user.profile.save()
            user.save()
            return redirect('login')
        errors = "Cannot create an account!"
    else:
        form = RegistrationForm()
    return render(request, "pages/register.html", {"form": form, "errors": errors})

@login_required
def logout_page(request):
    logout(request)
    return render(request, "pages/home.html")