from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, LibroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login, logout as do_logout

def createBook(request):
    # Creamos un formulario vacío
    form = LibroForm()

    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = LibroForm(request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            # Después de guardar redireccionamos a la lista
            return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "admin/createBook.html", {'form': form})


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
        #username  = form.cleaned_data.get("username")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        new_user  = User.objects.create_suscriptor(email, password) #quite el parametro "username"
        print(new_user)
        if new_user is not None:
            do_login(request, new_user)
            return redirect('/')
            #if new_user.is_superuser == 1:
            #    return render(request, "users/welcome.html")
            #else:
            #    return render(request, "users/home.html")

    return render(request, "users/register.html", context)


def welcome(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            return render(request, "users/welcome.html")
        else:
            return render(request, "users/home.html")
    return redirect('/login')


def logout(request):
    do_logout(request)
    return redirect('/')
