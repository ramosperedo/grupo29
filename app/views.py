from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import is_safe_url
from .forms import *
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login, logout as do_logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django import forms
from django.db.models.query import EmptyQuerySet
from django.db.models import Avg

import os, datetime


def listReportBooks(request):
    libros = Libro.objects.filter().order_by('-vistos')
    #paginator = Paginator(libros, 5)
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    return render(request, "admin/listReportBooks.html", {'libros': libros})

def listUsuarios(request):
    form = UserFilterForm()
    if request.method == "POST":
        form = UserFilterForm(request.POST)
        if form.is_valid():
            desde = form.cleaned_data['desde']
            hasta = form.cleaned_data['hasta']
            if desde > hasta:
                    messages.info(request, 'La fecha "desde" debe ser mayor a la de "hasta"')
                    return render(request, "admin/listUsuarios.html", {'form': form})
            else:
                usuarios = User.objects.filter(admin=False,dateCreate__lte=hasta,dateCreate__gte=desde).order_by('-id')
                return render(request, "admin/listUsuarios.html", {'form': form, 'usuarios': usuarios})            
    return render(request, "admin/listUsuarios.html", {'form': form})

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
    return render(request, "admin/editBook.html", {'form': form, 'obj':instancia})

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

def libros_activos(libros):
    now = datetime.date.today()
    librosActivos = Libro.objects.none()
    for libro in libros:
        cumple = Capitulo.objects.filter(idLibro=libro.id,fechaLanzamiento__lte=now,fechaVencimiento__gte=now)
        if cumple:
            librosActivos = librosActivos.union(Libro.objects.filter(id=libro.id))
            Libro.objects.filter(id=libro.id).update(fechaVencimientoFinal=cumple.first().fechaVencimiento)
    return librosActivos

def listBooks(request):
    libros = Libro.objects.filter().order_by('-vistos')
    if not request.user.admin:
        libros = libros_activos(libros)
    for libro in libros:
        actualiza = Capitulo.objects.filter(idLibro=libro.id).order_by('-fechaVencimiento')
        if actualiza:
            Libro.objects.filter(id=libro.id).update(fechaVencimientoFinal=actualiza.first().fechaVencimiento)
    paginator = Paginator(libros, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "shared/listOfBooks.html", {'libros': page_obj})

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

def loadLibroEnCapitulos(request, libro_id):
    if Libro.objects.get(id=libro_id).ultimoCapitulo:
        messages.info(request, 'El libro seleccionado ya se encuentra completo')
        return redirect('/listBooks')
    else:
        form = CapituloForm()
        form.fields['nombre'].required = True
        form.fields['numero'].required = True
        capitulos = Capitulo.objects.filter(idLibro=libro_id)
        if capitulos:
            numero = capitulos.order_by('-numero').first().numero
            form.fields['numero'].initial = numero + 1
        else:
            form.fields['numero'].initial = 1
        form.fields['idLibro'].initial = Libro.objects.get(id=libro_id)
        if request.method == "POST":
            form = CapituloForm(request.POST,request.FILES)
            if form.is_valid():
                fechaV = form.cleaned_data['fechaVencimiento']
                fechaL = form.cleaned_data['fechaLanzamiento']
                num = form.cleaned_data['numero']
                if fechaL > fechaV:
                    messages.info(request, 'La fecha de lanzamiento debe ser mayor a la de vencimiento')
                    return render(request, "admin/loadCapitulo.html", {'form': form})
                else:
                    if Capitulo.objects.filter(idLibro=libro_id,numero=num):
                        messages.info(request, 'Ya existe ese numero de capitulo')
                        return render(request, "admin/loadCapitulo.html", {'form': form})
                    instancia = form.save(commit=False)
                    ultimo = form.cleaned_data['ultimoCapitulo']
                    #Actualizamos el estado del libro (Si esta completo o no y las fechas de vencimiento)
                    if ultimo:
                        if Capitulo.objects.filter(idLibro = libro_id, numero__gte = num):
                            messages.info(request, 'El numero del ultimo capitulo debe ser el mayor')
                            return render(request, "admin/loadCapitulo.html", {'form': form})
                        Libro.objects.filter(id=libro_id).update(ultimoCapitulo=True)
                        Capitulo.objects.filter(idLibro=libro_id).update(fechaVencimiento=fechaV)
                    #Finalmente, almacenamos el nuevo-ultimo capitulo del libro
                    instancia.save()
                    Libro.objects.filter(id=libro_id).update(LibroEnCapitulos=True)
                    return redirect('/listBooks')
        return render(request, "admin/loadCapitulo.html", {'form': form})

def loadLibroCompleto(request, libro_id):
    if Libro.objects.get(id=libro_id).ultimoCapitulo and not Libro.objects.get(id=libro_id).LibroEnCapitulos:
        messages.info(request, 'El libro seleccionado ya se encuentra completo')
        return redirect('/listBooks')
    else:
        form = CapituloForm()
        form.fields['nombre'].widget = forms.HiddenInput()
        form.fields['numero'].widget = forms.HiddenInput()
        form.fields['ultimoCapitulo'].widget = forms.HiddenInput()
        form.fields['idLibro'].initial = Libro.objects.get(id=libro_id)
        if request.method == "POST":
            form = CapituloForm(request.POST,request.FILES)
            form.fields['nombre'].widget = forms.HiddenInput()
            form.fields['numero'].widget = forms.HiddenInput()
            form.fields['nombre'].required = False
            form.fields['numero'].required = False
            if form.is_valid():
                fechaV = form.cleaned_data['fechaVencimiento']
                fechaL = form.cleaned_data['fechaLanzamiento']
                if fechaL > fechaV:
                    messages.info(request, 'La fecha de lanzamiento debe ser mayor a la de vencimiento')
                    return render(request, "admin/loadCapitulo.html", {'form': form})
                else:
                    instancia = form.save(commit=False)
                    #Eliminamos todos los capitulos anteriores existentes para libro_id
                    Capitulo.objects.filter(idLibro=libro_id).delete()
                    #Actualizamos el estado del libro (Si esta completo o no)
                    Libro.objects.filter(id=libro_id).update(ultimoCapitulo=True, fechaVencimientoFinal=fechaV, LibroEnCapitulos=False)
                    #Capitulo.objects.filter(idLibro=libro_id).update(nombre="Libro Completo")
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
                    return redirect('/')
                else:
                    mis_perfiles=Perfil.objects.filter(idSuscriptor=request.user.id)
                    return render(request, "users/perfiles.html",{'perfiles':mis_perfiles})
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
            ## PerfilManager.create_perfil(nombre+apellido,new_user.id) --- Nose como lo usaban pero a mi no me funciona esto
            defaultPerfil = Perfil(idSuscriptor = new_user, nombre = nombre+apellido)
            defaultPerfil.save()
            actual = PerfilActual(idSuscriptor = new_user, idPerfil = defaultPerfil)
            actual.save()
            do_login(request, new_user)#si se llega a arreglar el orden es nombre, apellido, email, pass, idtarjeta
            return redirect('/')

    return render(request, "users/register.html", context)

def editarSuscriptor(request):#modificado para recibir solo su propio id
    instancia = User.objects.get(id=request.user.id)#aca tendria que ir sus_id si queremos modificar otro
    instancia2 = Tarjeta.objects.get(id=instancia.idTarjeta)
    form = SuscriptorForm(instance=instancia)
    form2 = TarjetaForm(instance=instancia2)
    if request.method == "POST":
        form = SuscriptorForm(request.POST, instance=instancia)
        form2 = TarjetaForm(request.POST, instance=instancia2)
        if form.is_valid() and form2.is_valid():
            instancia = form.save(commit=False)
            instancia2 = form2.save(commit=False)
            instancia.save()
            instancia2.save()
            messages.success(request, 'Se modificaron los datos exitosamente!!')
    return render(request, "users/editar.html", {'form': form,'form2': form2})

def editModeSuscripcion(request):
    mode = User.objects.get(id=request.user.id).premium
    if mode:
        if Perfil.objects.filter(idSuscriptor=request.user.id).count() < 3:
            User.objects.filter(id=request.user.id).update(premium=False)
        else:
            messages.success(request, 'Para realizar el cambio de modo debes tener como maximo 2 perfiles')
            return redirect('/editarSuscriptor')
    else:
        User.objects.filter(id=request.user.id).update(premium=True)
    datosSuscriptor = User.objects.get(pk=request.user.id)
    datosTarjeta = Tarjeta.objects.get(id=datosSuscriptor.idTarjeta)
    nombreTipoTarjeta = TipoTarjeta.objects.get(id=datosTarjeta.tipo)
    messages.success(request, 'Se realizo el cambio de modo exitosamente')
    return render(request, "shared/infoSuscriptor.html",{'datos':datosSuscriptor,'tarjeta':datosTarjeta,'tipo':nombreTipoTarjeta, 'mensaje':""})

def infoSuscriptor(request):
    try:
        datosSuscriptor = User.objects.get(pk=request.user.id)
        datosTarjeta = Tarjeta.objects.get(id=datosSuscriptor.idTarjeta)
        nombreTipoTarjeta = TipoTarjeta.objects.get(id=datosTarjeta.tipo)
    except Exception as e:
        return render(request, "shared/infoSuscriptor.html",{'mensaje':"ACCESO NO PERMITIDO"})

    if datosSuscriptor is not None:
        return render(request, "shared/infoSuscriptor.html",{'datos':datosSuscriptor,'tarjeta':datosTarjeta,'tipo':nombreTipoTarjeta, 'mensaje':""})
    else:
        return render(request, "shared/infoSuscriptor.html",{'mensaje':"no se encontro al suscriptor cod:2"})

def logout(request):
    do_logout(request)
    return redirect('/')

def busqueda(nombre="",autor="",genero="",editorial="",admin=0):
    BuscandoLibro = Libro.objects.filter(nombre__contains=nombre)
    now = datetime.date.today()
    librosActivos = Libro.objects.none()
    if admin == 0:
        for libro in BuscandoLibro:
            cumple = Capitulo.objects.filter(idLibro=libro.id,fechaLanzamiento__lte=now,fechaVencimiento__gte=now)
            if cumple:
                librosActivos = librosActivos.union(Libro.objects.filter(id=libro.id,))
        BuscandoLibro = librosActivos
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
    if autor+genero+editorial != "":
        print("queryset vacio antes de la interseccion")
        print(querysetvacio)
        BuscandoLibro = BuscandoLibro.intersection(querysetvacio)
        print("queryset vacio despues de la interseccion")
        print(querysetvacio)
    if BuscandoLibro.count() == 0:
        return ""
    else:
        return BuscandoLibro.order_by('id')

def administrarPerfiles(request):
    config = Configuracion.objects.all()
    mis_perfiles=Perfil.objects.filter(idSuscriptor=request.user.id)
    return render(request, "users/perfiles.html",{'config': config,
                                                  'perfiles':mis_perfiles,
                                                  'cantidad_perfiles':mis_perfiles.count()})

def createPerfil(request):
    form = PerfilForm()
    cantidad_perfiles=Perfil.objects.filter(idSuscriptor=request.user.id).count()
    bandera=0
    if request.user.premium and cantidad_perfiles > 4:
        bandera+=1
    if not request.user.premium and cantidad_perfiles > 2:
        bandera+=1
    if bandera == 0 :
        if request.method == "POST":
            form = PerfilForm(request.POST)
            if form.is_valid():
                instancia = form.save(commit = False)
                obj = Perfil(nombre = instancia.nombre , idSuscriptor = User.objects.get(id=request.user.id))
                obj.save()
                return redirect('/perfiles')
        return render(request, "users/createPerfil.html", {'form': form,'mensaje':''})
    else:
        return render(request, "users/createPerfil.html", {'form': form,'mensaje':'no se puede registrar mas de '+str(config.maximoPremium)+' perfiles en modalidad premium o '+str(config.maximoStandar)+' en la modalidad standar'})

def obtener_perfil(request):
    mi_perfil_actual=PerfilActual.objects.get(idSuscriptor=request.user.id)
    mi_perfil=Perfil.objects.get(id=mi_perfil_actual.idPerfil_id)
    return mi_perfil

def inicio(request):
    form = BuscadorForm(request.POST or None)
    if request.user.is_authenticated:
        resultado="-"
        if form.is_valid():
            nombre = form.cleaned_data.get("nombre")
            autor  = form.cleaned_data.get("autor")
            genero  = form.cleaned_data.get("genero")
            editorial  = form.cleaned_data.get("editorial")
            datos = nombre+autor+genero+editorial
            if datos !="":
                resultado = busqueda(nombre,autor,genero,editorial,request.user.is_superuser)
        paginator = Paginator(resultado, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if request.user.is_superuser == 1:
            return render(request, "users/welcome.html",{'form': form,'res':resultado,'page_obj': page_obj})
        else:
            mi_perfil=obtener_perfil(request)
            return render(request, "users/home.html",{'form': form,'res':resultado,'nombre':mi_perfil.nombre,'page_obj': page_obj})
    return redirect('/login')

def detalleLibro(request, libro_id):
    instancia = get_object_or_404(Libro, id = libro_id)
    capitulos = Capitulo.objects.all().filter(idLibro = libro_id)
    trailers = Trailer.objects.all().filter(idLibro = libro_id)
    reseñas = Review.objects.all().filter(idLibro = libro_id)
    puntaje = Review.objects.filter(idLibro = libro_id).aggregate(Avg('puntaje'))['puntaje__avg']
    if puntaje is None:
        puntaje = 0
    puedeReseñar = True
    if  request.user.is_superuser == 1:
        puedeReseñar = False
    context = {
        "obj" : instancia,
        "capitulos" : capitulos,
        "trailers" : trailers,
        "reseñas" : reseñas,
        "puedeReseñar" : puedeReseñar,
        "puntaje" : puntaje
        }
    if request.user.is_superuser != 1:
        perfilActual = PerfilActual.objects.get(idSuscriptor = request.user.id)
        idP = perfilActual.idPerfil
        context["favorito"] = Favorito.objects.filter(idPerfil = perfilActual.idPerfil).filter(idLibro = libro_id)
        context["id"] = idP
        context["capitulos"] = capitulos.filter(fechaLanzamiento__lte = datetime.date.today()).filter(fechaVencimiento__gte = datetime.date.today())
        context["abiertos"] = Historial.objects.all().filter(idPerfil = perfilActual.idPerfil).filter(terminado = False)
        context["terminados"] = Historial.objects.all().filter(idPerfil = perfilActual.idPerfil).filter(terminado = True)
        if instancia.ultimoCapitulo == False:
            context["puedeReseñar"] = False
        else:
            leidos = context["terminados"]
            for n in context["terminados"]:
                if n.idCapitulo.idLibro.id != libro_id:
                    leidos = leidos.exclude(idCapitulo = n.idCapitulo.id)
            if len(leidos) < len(Capitulo.objects.filter(idLibro = libro_id)):
                context["puedeReseñar"] = False
            elif len(Review.objects.filter(idLibro = libro_id).filter(idPerfil = perfilActual.idPerfil)) != 0:
                context["puedeReseñar"] = False
    return render (request, "shared/libroDetalle.html", context)

def marcarCapitulo(request, capitulo_id):
    actual = PerfilActual.objects.get(idSuscriptor = request.user.id)
    instance = Historial.objects.filter(idPerfil = actual.idPerfil).get(idCapitulo = capitulo_id)
    instance.terminado = True
    instance.save()
    return redirect('/viewBook/'+str(Capitulo.objects.get(id = capitulo_id).idLibro.id))

def leerCapitulo(request, capitulo_id):
    instance = Capitulo.objects.get(id = capitulo_id)
    disponible = True
    if (instance.fechaLanzamiento > datetime.date.today()):
        disponible = False
    if not request.user.is_superuser:
        if not Historial.objects.filter(idPerfil = PerfilActual.objects.get(idSuscriptor = request.user.id).idPerfil).filter(idCapitulo = Capitulo.objects.get(id = capitulo_id)).exists():
            marca = Historial(idPerfil = PerfilActual.objects.get(idSuscriptor = request.user.id).idPerfil, idCapitulo = Capitulo.objects.get(id =capitulo_id))
            marca.save()
    context = {
        "obj" : instance,
        "disponible" : disponible
    }
    return render (request, "shared/leerCapitulo.html", context)

def editBookFiles(request, libro_id):
    obj = Libro.objects.get(id = libro_id)
    capitulos = Capitulo.objects.all().filter(idLibro = libro_id)
    d1 = datetime.datetime(datetime.MINYEAR,1,1)
    d2 = datetime.datetime(2029,12,31)
    instancia = {
        "fechaLanzamiento" : d1,
        "fechaVencimiento" : d2
    }
    form = ModificarFechasForm(initial = instancia)
    context = {
        "obj" : obj,
        "capitulos" : capitulos,
        "form" : form
    }
    if request.method == "POST":
        form = ModificarFechasForm(request.POST)
        if form.is_valid():
            fl = form.cleaned_data.get("fechaLanzamiento")
            fv = form.cleaned_data.get("fechaVencimiento")
            print(fl)
            print(date.today())
            if fl < date.today():
                messages.info(request, 'La fecha de lanzamiento debe ser mayor a la actual')
                return render(request, "admin/editBookFiles.html", context)
            if fv < date.today():
                messages.info(request, 'La fecha de vencimiento debe ser mayor a la actual')
                return render(request, "admin/editBookFiles.html", context)
            if (fl > fv):
                messages.info(request, 'La fecha de lanzamiento debe ser mayor a la de vencimiento')
                return render(request, "admin/editBookFiles.html", context)
            Capitulo.objects.filter(idLibro = Libro.objects.get(id = libro_id)).update(fechaLanzamiento = fl,fechaVencimiento = fv)
            return redirect('/editBookFiles/'+str(libro_id))
    return render(request, "admin/editBookFiles.html", context)

def editCapitulo(request, capitulo_id):
    instancia = Capitulo.objects.get(id=capitulo_id)
    libro = instancia.idLibro
    idLibro = libro.id
    original = instancia.archivo
    form = CapituloForm(instance=instancia)
    form.fields['nombre'].required = True
    form.fields['numero'].required = True
    if libro.ultimoCapitulo:
        form.fields['fechaLanzamiento'].widget = forms.HiddenInput()
        form.fields['fechaVencimiento'].widget = forms.HiddenInput()
    form.fields['ultimoCapitulo'].widget = forms.HiddenInput()
    if request.method == "POST":
        form = CapituloForm(request.POST,request.FILES, instance=instancia)
        if libro.ultimoCapitulo:
            form.fields['fechaLanzamiento'].widget = forms.HiddenInput()
            form.fields['fechaVencimiento'].widget = forms.HiddenInput()
        form.fields['ultimoCapitulo'].widget = forms.HiddenInput()
        if form.is_valid():
            fechaV = form.cleaned_data['fechaVencimiento']
            fechaL = form.cleaned_data['fechaLanzamiento']
            num = form.cleaned_data['numero']
            nombre = form.cleaned_data['nombre']
            archivo = form.cleaned_data['archivo']
            if Capitulo.objects.filter(idLibro=libro.id,numero=num) and (not Capitulo.objects.filter(id=capitulo_id,numero=num)):
                        messages.info(request, 'Ya existe ese numero de capitulo')
                        return render(request, "admin/editCapitulo.html", {'form': form})
            if not libro.ultimoCapitulo:
                if fechaL > fechaV:
                    messages.info(request, 'La fecha de lanzamiento debe ser mayor a la de vencimiento')
                    return render(request, "admin/editCapitulo.html", {'form': form})
                if original != archivo:
                    Historial.objects.filter(idCapitulo_id = capitulo_id).update(terminado = False)
                    instancia.archivo.save(archivo.name,archivo,save = True)
                Capitulo.objects.filter(id=capitulo_id).update(nombre=nombre,numero=num,fechaVencimiento=fechaV,fechaLanzamiento=fechaL)
            else:
                ultiCap = Capitulo.objects.get(idLibro=libro.id,ultimoCapitulo=True)
                if ultiCap.id == capitulo_id:
                    if original != archivo:
                        Historial.objects.filter(idCapitulo_id = capitulo_id).update(terminado = False)
                        instancia.archivo.save(archivo.name,archivo,save = True)
                    Capitulo.objects.filter(id=capitulo_id).update(nombre=nombre,numero=num)
                else:
                    if ultiCap.numero < num:
                        messages.info(request, 'El numero de capitulo debe ser menor al numero de capitulo final')
                        return render(request, "admin/editCapitulo.html", {'form': form})
                    if original != archivo:
                        Historial.objects.filter(idCapitulo_id = capitulo_id).update(terminado = False)
                        instancia.archivo.save(archivo.name,archivo,save = True)
                    Capitulo.objects.filter(id=capitulo_id).update(nombre=nombre,numero=num)
            return redirect('/listBooks')
    return render(request, "admin/editCapitulo.html", {'form': form, 'obj':instancia, 'idLibro':idLibro})

def deleteCapitulo(request, capitulo_id):
    obj = Capitulo.objects.get(id = capitulo_id)
    libro = obj.idLibro
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        os.remove(os.path.join(BASE_DIR,obj.archivo.url.replace('/','\\')))
    except:
        print('ya estaba borrado?')
    obj.delete()
    if libro.ultimoCapitulo:
        Libro.objects.filter(id=libro.id).update(ultimoCapitulo=False)
    if len(Capitulo.objects.filter(idLibro = libro)) == 0:
        Libro.objects.filter(id=libro.id).update(fechaVencimientoFinal=None)
    return redirect('/listBooks')

def editFechaLibro(request, obj_id):
    cap = Capitulo.objects.filter(idLibro=obj_id).order_by("-fechaVencimiento").first()
    form = FechasLibroForm()
    form.fields['fechaVencimiento'].initial = cap.fechaVencimiento
    form.fields['fechaLanzamiento'].initial = cap.fechaLanzamiento
    if request.method == "POST":
        form = FechasLibroForm(request.POST)
        if form.is_valid():
            fechaV = form.cleaned_data['fechaVencimiento']
            fechaL = form.cleaned_data['fechaLanzamiento']
            if fechaL > fechaV:
                messages.info(request, 'La fecha de lanzamiento no debe ser mayor a la de vencimiento')
                return render(request, "admin/editFechaLibro.html", {'form': form})
            else:
                Capitulo.objects.filter(idLibro=obj_id).update(fechaVencimiento=fechaV,fechaLanzamiento=fechaL)
                return redirect('/listBooks')
    return render(request, "admin/editFechaLibro.html", {'form': form})

""" 
esta es la consulta sql del historial
SELECT 
app_historial.id,
app_capitulo.id,
app_libro.id,
app_historial.id AS historial_id,
app_capitulo.id AS capitulo_id,
app_libro.id AS libro_id, 
app_capitulo.nombre AS capitulo_nombre,
app_libro.nombre AS libro_nombre,
app_capitulo.fechaLanzamiento,
app_capitulo.fechaVencimiento 
FROM 
app_historial,app_capitulo,app_libro 
WHERE 
app_historial.idCapitulo_id = app_capitulo.id AND 
app_capitulo.idLibro_id = app_libro.id AND 
app_historial.idPerfil_id = 1    
"""
def historial(request):
    lista = [] 
    now = datetime.date.today()
    nombre_temporal=""
    mensaje="no se encontro resultados"
    perfil_actual = PerfilActual.objects.get(idSuscriptor=request.user.id).idPerfil_id
    resultado = Libro.objects.raw("SELECT app_historial.id,app_capitulo.id,app_libro.id,app_historial.id AS historial_id,app_capitulo.id AS capitulo_id,app_libro.id AS libro_id, app_capitulo.nombre AS capitulo_nombre,app_libro.nombre AS libro_nombre,app_capitulo.fechaLanzamiento,app_capitulo.fechaVencimiento,app_historial.terminado FROM app_historial,app_capitulo,app_libro WHERE app_historial.idCapitulo_id = app_capitulo.id AND app_capitulo.idLibro_id = app_libro.id AND app_historial.idPerfil_id = "+str(perfil_actual))
    for obj in resultado:
        if obj.fechaLanzamiento <= now and obj.fechaVencimiento > now :
            datos = {
                        "historial_id": obj.historial_id,
                        "capitulo_id": obj.capitulo_id,
                        "libro_id": obj.libro_id,
                        "capitulo_nombre": obj.capitulo_nombre,
                        "libro_nombre": obj.libro_nombre if (obj.libro_nombre != nombre_temporal) else "",
                        "fechaLanzamiento": obj.fechaLanzamiento,
                        "fechaVencimiento": obj.fechaVencimiento,
                        "terminado": obj.terminado
                        }
            lista.append(datos)
            nombre_temporal = obj.libro_nombre
            mensaje=""
        print (obj.libro_id,"-",obj.capitulo_nombre,"-",obj.fechaLanzamiento,"-",obj.fechaVencimiento)
    for dato in lista:
        print (dato)
    paginator = Paginator(lista, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "users/historial.html",{'libros':lista,'mensaje':mensaje,'page_obj': page_obj})
    
def selectperfil(request,perfil_id):
    PerfilActual.objects.filter(idSuscriptor=request.user.id).update(idPerfil=perfil_id)
    return redirect('/')

def eliminarperfil(request,perfil_id):
    mis_perfiles = Perfil.objects.filter(idSuscriptor=request.user.id)
    if mis_perfiles.count() > 1:
        if PerfilActual.objects.filter(idSuscriptor=request.user.id).first().idPerfil_id == perfil_id:
            for dato in mis_perfiles:
                if dato.id != perfil_id:
                    PerfilActual.objects.filter(idSuscriptor=request.user.id).update(idPerfil=dato.id)
        Perfil.objects.filter(id=perfil_id).delete()
    return redirect('/perfiles')

def createReview(request,libro_id):
    form = ReviewForm()
    actual = PerfilActual.objects.get(idSuscriptor = request.user.id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            puntaje = form.cleaned_data.get("puntaje")
            texto = form.cleaned_data.get("texto")
            spoiler = form.cleaned_data.get("spoiler")
            obj = Review(texto = texto , puntaje = puntaje, spoiler = spoiler, idPerfil = Perfil.objects.get(id = actual.idPerfil.id), idLibro = Libro.objects.get(id = libro_id), nombre = Perfil.objects.get(id = actual.idPerfil.id).nombre)
            obj.save()
            return redirect('/viewBook/' + str(libro_id))
    return render(request, "users/createReview.html", {'form': form,'id':libro_id})

def editReview(request,libro_id):
    actual = PerfilActual.objects.get(idSuscriptor = request.user.id)
    reseña = Review.objects.filter(idLibro = libro_id).get(idPerfil = Perfil.objects.get(id = actual.idPerfil.id))
    instancia = {
        'puntaje' : reseña.puntaje,
        'texto' : reseña.texto,
        'spoiler' : reseña.spoiler
    }
    form = ReviewForm(initial = instancia)
    bloqueada = reseña.spoilerAdmin
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            puntaje = form.cleaned_data.get("puntaje")
            texto = form.cleaned_data.get("texto")
            spoiler = form.cleaned_data.get("spoiler")
            reseña.puntaje = puntaje
            reseña.texto = texto
            if not reseña.spoilerAdmin:
                reseña.spoiler = spoiler
            reseña.save()
            return redirect('/viewBook/' + str(libro_id))
    return render(request, "users/editReview.html", {'form': form,'id':libro_id,'bloqueada':bloqueada})

def marcarSpoilerAdmin(request, review_id):
    obj = Review.objects.get(id = review_id)
    obj.spoiler = True
    obj.spoilerAdmin = True
    obj.save()
    return redirect('/viewBook/' + str(obj.idLibro.id))

def deleteReview(request, review_id):
    obj = Review.objects.get(id = review_id)
    libro_id = str(obj.idLibro.id)
    obj.delete()
    return redirect('/viewBook/' + libro_id)

def favorito(request, libro_id):
    if len(Favorito.objects.filter(idPerfil = PerfilActual.objects.get(idSuscriptor = request.user.id).idPerfil).filter(idLibro = libro_id)) == 0:
        obj = Favorito(idPerfil = PerfilActual.objects.get(idSuscriptor = request.user.id).idPerfil, idLibro = Libro.objects.get(id = libro_id))
        obj.save()
    else:
        obj = Favorito.objects.filter(idPerfil = PerfilActual.objects.get(idSuscriptor = request.user.id).idPerfil).get(idLibro = libro_id)
        obj.delete()
    return redirect('/viewBook/' + str(libro_id))

def listado_favoritos(request):
    perfil_actual = PerfilActual.objects.get(idSuscriptor=request.user.id).idPerfil_id
    favorito_con_nombre = Libro.objects.raw("SELECT * FROM app_favorito,app_libro WHERE app_favorito.idLibro_id = app_libro.id AND app_favorito.idPerfil_id = "+str(perfil_actual))
    cantidad = len(list(favorito_con_nombre))
    return render(request, "users/favoritos.html", {'datos': favorito_con_nombre,'cantidad':cantidad })
    
def eliminar_suscriptor(request):
    User.objects.filter(id=request.user.id).delete()
    return redirect('/')
