from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import is_safe_url
from .forms import RegisterForm, RegisterForm2, RegisterForm3, LibroForm, AutorForm, GeneroForm, EditorialForm, CapituloForm, NovedadForm, TrailerForm, SuscriptorForm, TarjetaForm, TipoTarjetaForm, PerfilForm, BuscadorForm
from .models import Configuracion, Libro, Capitulo, Novedad, Trailer, Autor, Editorial, Genero, TarjetaManager, Tarjeta, TipoTarjeta, Perfil, PerfilManager
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login, logout as do_logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models.query import EmptyQuerySet
import os, datetime


def createBook(request):
    # Creamos un formulario vacío
    form = LibroForm()
    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = LibroForm(request.POST,request.FILES)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            # Después de guardar redireccionamos a la lista
            return redirect('/listBooks')
    # Si llegamos al final renderizamos el formulario
    return render(request, "admin/createBook.html", {'form': form})

def editBook(request, libro_id):
    # Recuperamos la instancia de la persona
    instancia = Libro.objects.get(id=libro_id)
    # Creamos el formulario con los datos de la instancia
    form = LibroForm(instance=instancia)
    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Actualizamos el formulario con los datos recibidos
        form = LibroForm(request.POST,request.FILES, instance=instancia)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            # Después de guardar redireccionamos a la lista
            return redirect('/listBooks')
    # Si llegamos al final renderizamos el formulario
    return render(request, "admin/editBook.html", {'form': form})

def deleteBook(request, libro_id):
    # Recuperamos la instancia de la persona y la borramos
    instancia = Libro.objects.get(id=libro_id)
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.remove(os.path.join(BASE_DIR,instancia.foto.url.replace('/','\\')))
    except Exception as e:
        pass
    instancia.delete()
    # Después redireccionamos de nuevo a la lista
    return redirect('/listBooks')

def listBooks(request):
    now = datetime.date.today()
    libros = Libro.objects.all().order_by('vistos')
    librosActivos = []
    for libro in libros:
        cumple = Capitulo.objects.filter(idLibro=libro.id,fechaLanzamiento__lte=now,fechaVencimiento__gte=now)
        if cumple:
            librosActivos.append(libro)
            Libro.objects.filter(id=libro.id).update(fechaVencimientoFinal=cumple.first().fechaVencimiento)
    capitulos = Capitulo.objects.all()
    paginator = Paginator(libros, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "shared/listOfBooks.html", {'libros': page_obj, 'librosActivos': librosActivos})

def createAutor(request):
    form = AutorForm()
    if request.method == "POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listAutores')
    return render(request, "admin/createAutor.html", {'form': form})

def deleteAutor(request, autor_id):
    instancia = Autor.objects.get(id=autor_id)
    if Libro.objects.filter(idAutor=autor_id):
        messages.info(request, 'No se pudo eliminar el autor, revise que no existan libros que lo incluyan')
    else:
        instancia.delete()
    return redirect('/listAutores')

def listAutores(request):
    autores = Autor.objects.all()
    return render(request, "admin/listOfAutores.html", {'autores': autores})

def createGenero(request):
    form = GeneroForm()
    if request.method == "POST":
        form = GeneroForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listGeneros')
    return render(request, "admin/createGenero.html", {'form': form})

def deleteGenero(request, genero_id):
    instancia = Genero.objects.get(id=genero_id)
    if Libro.objects.filter(idGenero=genero_id):
        messages.info(request, 'No se pudo eliminar el genero, revise que no existan libros que lo incluyan')
    else:
        instancia.delete()
    return redirect('/listGeneros')

def listGeneros(request):
    generos = Genero.objects.all()
    return render(request, "admin/listOfGeneros.html", {'generos': generos})

def createEditorial(request):
    form = EditorialForm()
    if request.method == "POST":
        form = EditorialForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listEditoriales')
    return render(request, "admin/createEditorial.html", {'form': form})

def deleteEditorial(request, editorial_id):
    instancia = Editorial.objects.get(id=editorial_id)
    if Libro.objects.filter(idEditorial=editorial_id):
        messages.info(request, 'No se pudo eliminar la editorial, revise que no existan libros que la incluyan')
    else:
        instancia.delete()
    return redirect('/listEditoriales')

def listEditoriales(request):
    editoriales = Editorial.objects.all()
    return render(request, "admin/listOfEditoriales.html", {'editoriales': editoriales})

def createNovedad(request):
    form = NovedadForm()
    if request.method == "POST":
        form = NovedadForm(request.POST,request.FILES)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listNovedades')
    return render(request, "admin/createNovedad.html", {'form': form})

def editNovedad(request, novedad_id):
    instancia = Novedad.objects.get(id=novedad_id)
    form = NovedadForm(instance=instancia)
    if request.method == "POST":
        form = NovedadForm(request.POST,request.FILES, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listNovedades')
    return render(request, "admin/editNovedad.html", {'form': form})

def deleteNovedad(request, novedad_id):
    instancia = Novedad.objects.get(id=novedad_id)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        os.remove(os.path.join(BASE_DIR,instancia.archivo.url.replace('/','\\')))
    except Exception as e:
        pass
    try:
        os.remove(os.path.join(BASE_DIR,instancia.archivoVideo.url.replace('/','\\')))
    except Exception as e:
        pass
    instancia.delete()
    return redirect('/listNovedades')

def viewNovedad(request, novedad_id):
    instancia = get_object_or_404(Novedad, id = novedad_id)
    context = {
        "obj" : instancia
        }
    return render (request, "shared/novedad.html", context)

def listNovedades(request):
    novedades = Novedad.objects.all()
    paginator = Paginator(novedades, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shared/listOfNovedades.html', {'novedades': page_obj})

def createTrailer(request):
    form = TrailerForm()
    if request.method == "POST":
        form = TrailerForm(request.POST,request.FILES)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listTrailers')
    return render(request, "admin/createTrailer.html", {'form': form})

def editTrailer(request, trailer_id):
    instancia = Trailer.objects.get(id=trailer_id)
    form = TrailerForm(instance=instancia)
    if request.method == "POST":
        form = TrailerForm(request.POST,request.FILES, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listTrailers')
    return render(request, "admin/editTrailer.html", {'form': form})

def deleteTrailer(request, trailer_id):
    instancia = Trailer.objects.get(id=trailer_id)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        os.remove(os.path.join(BASE_DIR,instancia.archivo.url.replace('/','\\')))
    except Exception as e:
        pass
    try:
        os.remove(os.path.join(BASE_DIR,instancia.archivoVideo.url.replace('/','\\')))
    except Exception as e:
        pass
    instancia.delete()
    return redirect('/listTrailers')

def viewTrailer(request, trailer_id):
    instancia = get_object_or_404(Trailer, id = trailer_id)
    context = {
        "obj" : instancia
        }
    return render (request, "shared/trailer.html", context)

def listTrailers(request):
    trailers = Trailer.objects.all()
    paginator = Paginator(trailers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shared/listOfTrailers.html', {'trailers': page_obj})

def loadFile(request, libro_id):
    return render(request, "admin/loadFile.html", {'libro_id': libro_id})

def loadLibroEnCapitulos(request, libro_id):
    form = CapituloForm()
    form2 = RegisterForm3()
    capitulos = Capitulo.objects.filter(idLibro=libro_id)
    if capitulos:
        numero = capitulos.order_by('-numero').first().numero
        form.fields['numero'].initial = numero + 1
    else:
        form.fields['numero'].initial = 1
    form.fields['idLibro'].initial = Libro.objects.get(id=libro_id)
    form2.fields['premium'].label = 'Seleccione aca si es el ultimo capitulo'
    if request.method == "POST":
        form = CapituloForm(request.POST,request.FILES)
        form2 = RegisterForm3(request.POST)
        if form.is_valid() and form2.is_valid():
            fechaV = form.cleaned_data['fechaVencimiento']
            instancia = form.save(commit=False)
            completo = form2.cleaned_data.get("premium")
            #Actualizamos el estado del libro (Si esta completo o no y las fechas de vencimiento)
            if completo:
                Libro.objects.filter(id=libro_id).update(ultimoCapitulo=True)
                Capitulo.objects.filter(idLibro=libro_id).update(fechaVencimiento=fechaV)
            #Finalmente, almacenamos el nuevo-ultimo capitulo del libro
            instancia.save()
            return redirect('/listBooks')
    return render(request, "admin/loadCapitulo.html", {'form': form, 'form2':form2})

def loadLibroCompleto(request, libro_id):
    form = CapituloForm()
    if request.method == "POST":
        form = CapituloForm(request.POST,request.FILES)
        form.fields['idLibro'].initial = Libro.objects.get(id=libro_id)
        if form.is_valid():
            fechaV = form.cleaned_data['fechaVencimiento']
            fechaL = form.cleaned_data['fechaLanzamiento']
            instancia = form.save(commit=False)
            #Eliminamos todos los capitulos anteriores existentes para libro_id
            Capitulo.objects.filter(idLibro=libro_id).delete()
            #Actualizamos el estado del libro (Si esta completo o no)
            Libro.objects.filter(id=libro_id).update(ultimoCapitulo=True, fechaLanzamientoFinal=fechaL, fechaVencimientoFinal=fechaV)
            #Finalmente, almacenamos el nuevo-ultimo capitulo del libro
            instancia.save()
            return redirect('/listBooks')
    return render(request, "admin/loadCapitulo.html", {'form': form})

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
                    return render(request, "users/perfiles.html")
    return render(request, "users/login.html", {'form': form})

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None)
    form2 = RegisterForm2(request.POST or None)
    form3 = RegisterForm3(request.POST or None)
    context = {
        "form": form, "form2": form2, "form3": form3
    }
    if form.is_valid() and form2.is_valid() and form3.is_valid():
        nombre = form.cleaned_data.get("nombre")
        apellido  = form.cleaned_data.get("apellido")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        premium = form3.cleaned_data.get("premium")
        tipo = form2.cleaned_data.get("tipo")
        dni = form2.cleaned_data.get("dni")
        numero = form2.cleaned_data.get("numero")
        clave = form2.cleaned_data.get("clave")
        fechaVencimiento = form2.cleaned_data.get("fechaVencimiento")
        new_tarj = TarjetaManager.create_tarjeta(dni,numero,clave,fechaVencimiento,tipo)
        new_user  = User.objects.create_suscriptor(nombre, apellido, email, premium, password,new_tarj.id)
        print(new_user)#en la anterior linea el orden de los datos del usuario no son en ese orden
        if new_user is not None:#pero por un bug raro lo tube que cambiar para que registre bien
            PerfilManager.create_perfil(nombre+apellido,new_user.id)
            do_login(request, new_user)#si se llega a arreglar el orden es nombre, apellido, email, pass, idtarjeta
            return redirect('/')

    return render(request, "users/register.html", context)

def editarSuscriptor(request, sus_id):#modificado para recibir solo su propio id
    instancia = User.objects.get(id=request.user.id)#aca tendria que ir sus_id si queremos modificar otro
    instancia2 = Tarjeta.objects.get(id=instancia.idTarjeta)
    form = SuscriptorForm(instance=instancia)
    form2 = TarjetaForm(instance=instancia2)
    #form3 = RegisterForm3(request.POST or None)
    if request.method == "POST":
        form = SuscriptorForm(request.POST, instance=instancia)
        form2 = TarjetaForm(request.POST, instance=instancia2)
        if form.is_valid() and form2.is_valid():
            instancia = form.save(commit=False)
            instancia2 = form2.save(commit=False)
            instancia.save()
            instancia2.save()
            messages.success(request, 'se modificó sus datos!!')
    return render(request, "users/editar.html", {'form': form,'form2': form2})

def infoSuscriptor(request, num=0):
    try:
        datosSuscriptor = User.objects.get(pk=num)
        print(datosSuscriptor.email)
        datosTarjeta = Tarjeta.objects.get(id=datosSuscriptor.idTarjeta)
        print(datosTarjeta.dni)
        nombreTipoTarjeta = TipoTarjeta.objects.get(id=datosTarjeta.tipo)
        print(nombreTipoTarjeta.nombre)
    except Exception as e:
        return render(request, "shared/infoSuscriptor.html",{'mensaje':"ACCESO NO PERMITIDO"})

    if request.user.id == num:
        if datosSuscriptor is not None:
            return render(request, "shared/infoSuscriptor.html",{'datos':datosSuscriptor,'tarjeta':datosTarjeta,'tipo':nombreTipoTarjeta, 'mensaje':""})
        else:
            return render(request, "shared/infoSuscriptor.html",{'mensaje':"no se encontro al suscriptor cod:2"})
    else:
        return render(request, "shared/infoSuscriptor.html",{'mensaje':"no se encontro al suscriptor cod:3"})

def logout(request):
    do_logout(request)
    return redirect('/')

def busqueda(nombre="",autor="",genero="",editorial="",admin=0):
    #averiguar si buscar una cadena vacia implica algun resultado
    BuscandoLibro = Libro.objects.filter(nombre__contains=nombre)
    print (BuscandoLibro)
    querysetvacio = Libro.objects.none()
    print (querysetvacio)
    if autor != "":
        BuscandoAutor = Autor.objects.filter(nombre__contains=autor)
        if BuscandoAutor is not None:
            for autores in BuscandoAutor:
                print (autores.id)
                temp = BuscandoLibro.filter(idAutor=autores.id)
                print (temp)
                querysetvacio = querysetvacio.union(temp)
            print ('aca esta el queryset recolector de autor')
            print (querysetvacio)
    if genero != "":
        BuscandoGenero = Genero.objects.filter(nombre__contains=genero)
        print (BuscandoLibro)
        print (BuscandoGenero)
        if BuscandoGenero is not None:
            for generos in BuscandoGenero:
                print (generos.id)
                temp = BuscandoLibro.filter(idGenero=generos.id)
                print (temp)
                querysetvacio = querysetvacio.union(temp)
            print ('aca esta el queryset recolector de genero')
            print (querysetvacio)
    if editorial != "":
        BuscandoEditorial = Editorial.objects.filter(nombre__contains=editorial)
        print (BuscandoLibro)
        print (BuscandoEditorial)
        if BuscandoEditorial is not None:
            for editoriales in BuscandoEditorial:
                print (editoriales.id)
                temp = BuscandoLibro.filter(idEditorial=editoriales.id)
                print (temp)
                querysetvacio = querysetvacio.union(temp)
            print ('aca esta el queryset recolector de editorial')
            print (querysetvacio)
    print (BuscandoLibro)
    if isinstance(querysetvacio, EmptyQuerySet):
        querysetvacio = BuscandoLibro
    else:
        BuscandoLibro = BuscandoLibro.intersection(querysetvacio)
    if BuscandoLibro.count() == 0:
        return ""
    else:
        return BuscandoLibro

def administrarPerfiles(request):
    config = Configuracion.objects.all()
    return render(request, "users/perfiles.html",{'config': config})

def createPerfil(request):
    form = PerfilForm()
    if request.method == "POST":
        form = CapituloForm(request.POST)
        form.fields['idSuscriptor'].initial = User.objects.get(id=request.user.id)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/administrarPerfiles')
    return render(request, "users/createPerfil.html", {'form': form})

def inicio(request):
    form = BuscadorForm(request.POST or None)
    if request.user.is_authenticated:
        resultado=""
        if form.is_valid():
            nombre = form.cleaned_data.get("nombre")
            autor  = form.cleaned_data.get("autor")
            genero  = form.cleaned_data.get("genero")
            editorial  = form.cleaned_data.get("editorial")
            resultado = busqueda(nombre,autor,genero,editorial,request.user.is_superuser)
        if request.user.is_superuser == 1:
            return render(request, "users/welcome.html",{'form': form,'res':resultado})
        else:
            return render(request, "users/home.html",{'form': form,'res':resultado})
    return redirect('/login')
