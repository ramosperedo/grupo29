from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm #, UserCreationForm
from django.contrib.auth import login as do_login, logout as do_logout
from app.models import TarjetaManager
#from django.contrib.auth import logout as do_logout

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                if request.user.is_superuser == 1:
                    return render(request, "users/welcome.html")
                else:
                    return render(request, "users/home.html")
    return render(request, "users/login.html", {'form': form})

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        nombre = form.cleaned_data.get("nombre")
        apellido  = form.cleaned_data.get("apellido")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")

        tipo = form.cleaned_data.get("tipo")

        dni = form.cleaned_data.get("dni")
        numero = form.cleaned_data.get("numero")
        clave = form.cleaned_data.get("clave")
        fechaVencimiento = form.cleaned_data.get("fechaVencimiento")
        form.revisandoDatosTarjeta(dni,numero,clave,fechaVencimiento)

        new_tarj = TarjetaManager.create_tarjeta(dni,numero,clave,fechaVencimiento,tipo)
        new_user  = User.objects.create_suscriptor(nombre, apellido, email, password,new_tarj.id)
        print(new_user)
        if new_user is not None:
            do_login(request, new_user)
            return redirect('/')

    return render(request, "users/register.html", context)


def welcome(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            return render(request, "users/welcome.html")
        else:
            return render(request, "users/home.html")
    return redirect('/login')

def test(request):
    return render(request,"users/test.html")
"""
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                do_login(request, user)
                return redirect('/')

    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    return render(request, "users/register.html", {'form': form})


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return redirect('/')
    return render(request, "users/login.html", {'form': form})

"""
def logout(request):
    do_logout(request)
    return redirect('/')
