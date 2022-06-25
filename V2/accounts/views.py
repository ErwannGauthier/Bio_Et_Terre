from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect

User = get_user_model()
# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        valide = True
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        try:
            validate_email(email)
        except ValidationError as error:
            valide = False
            for e in error:
                messages.error(request, e)

        queryUser = User.objects.filter(email=email)
        if queryUser:
            valide = False
            messages.error(request, "Cette adresse mail est déjà utilisée.")

        if password != confirm_password:
            valide = False
            messages.error(request, "Saisissez deux fois le même mot de passe.")

        if valide:
            user = User.objects.create_user(username=email, password=password, first_name=firstname, last_name=lastname, email=email)
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/signup.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        queryUser = User.objects.filter(email=email)
        if queryUser:
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Mauvais mot de passe.")
        else:
            messages.error(request, "Aucun compte ne correspond à cette adresse mail.")

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')
