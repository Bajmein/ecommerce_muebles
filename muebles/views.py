from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .forms import RegistroForm
from .models import Carrito, ItemCarrito, Compra, ItemCompra, Categoria, Producto


# Pagina principal ----------------------------------------------------------------------------
def home(request):
    return render(request, "home.html")


# Usuarios -------------------------------------------------------------------------------------
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            if not Carrito.objects.filter(usuario=usuario).exists():
                Carrito.objects.create(usuario=usuario)
            return redirect('inicio_sesion')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def inicio_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('historial_compras')
    else:
        form = AuthenticationForm()
    return render(request, 'inicio_sesion.html', {'form': form})


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('/')


@login_required
def historial_compras(request):
    compras = request.user.compras.prefetch_related('items')
    return render(request, 'historial_compras.html', {'user': request.user, 'compras': compras})


# muebles --------------------------------------------------------------------------------------
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})


def listar_muebles_por_categoria(request, categoria):
    categoria_obj = Categoria.objects.filter(nombre=categoria).first()
    if not categoria_obj:
        return HttpResponse("Categoría no encontrada", status=404)

    muebles = Producto.objects.filter(categoria=categoria_obj)
    return render(request, 'muebles_categorias.html', {'categoria': categoria, 'muebles': muebles})


def buscar_muebles(request):
    query = request.GET.get('q', '').strip()
    resultados = []

    if query:
        resultados = Producto.objects.filter(nombre__icontains=query)

    return render(request, 'resultados_busqueda.html', {'query': query, 'resultados': resultados})


# Modelo ML ------------------------------------------------------------------------------------
def vectorizar_descripciones(muebles):
    descripciones = [f"{mueble.nombre} {mueble.descripcion or ''}" for mueble in muebles]
    vectorizador = TfidfVectorizer()
    matriz_tfidf = vectorizador.fit_transform(descripciones)
    return vectorizador, matriz_tfidf


def buscar_muebles_similares(consulta, muebles, mueble_id=None, n_resultados=3):
    muebles_lista = list(muebles)
    vectorizador, matriz_tfidf = vectorizar_descripciones(muebles_lista)
    consulta_vectorizada = vectorizador.transform([consulta])
    similitudes = cosine_similarity(consulta_vectorizada, matriz_tfidf)
    indices_similares = np.argsort(similitudes[0])[-n_resultados:][::-1]
    resultados = []
    for i in indices_similares:
        mueble = muebles_lista[i]
        if mueble_id is not None and mueble.nombre == mueble_id:
            continue
        resultados.append({"mueble": mueble})
        if len(resultados) == n_resultados:
            break
    return resultados


def detalle_mueble_por_categoria(request, categoria, mueble_nombre):
    categoria_obj = Categoria.objects.filter(nombre=categoria).first()
    if not categoria_obj:
        return HttpResponse("Categoría no encontrada", status=404)

    productos = Producto.objects.filter(categoria=categoria_obj)  # Asegúrate de manejar esto adecuadamente
    mueble = productos.filter(nombre=mueble_nombre).first()
    if not mueble:
        return HttpResponse("Mueble no encontrado", status=404)

    similares = buscar_muebles_similares(mueble.nombre, productos, mueble_id=mueble.id, n_resultados=4)
    return render(request, 'detalle_mueble_categoria.html', {
        'categoria': categoria,
        'mueble': mueble,
        'similares': similares
    })


# Carrito de compra ------------------------------------------------------------------------
def agregar_al_carrito(request, categoria, producto_nombre):
    if not request.user.is_authenticated:
        return redirect('inicio_sesion')

    producto = Producto.objects.filter(nombre=producto_nombre, categoria__nombre=categoria).first()
    if not producto:
        messages.error(request, "Producto no encontrado.")
        return redirect('listar_muebles_por_categoria', categoria=categoria)

    carrito = request.user.carrito
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'precio': producto.precio, 'imagen': producto.imagen}
    )
    if not created:
        item.cantidad += 1
        item.save()

    messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect('listar_muebles_por_categoria', categoria=categoria)


@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(item.subtotal() for item in items)
    return render(request, 'carrito.html', {'items': items, 'total': total})


@login_required
def eliminar_del_carrito(request, item_id):
    if not request.user.is_authenticated:
        return redirect('inicio_sesion')

    item = ItemCarrito.objects.filter(id=item_id, carrito=request.user.carrito).first()
    if item:
        item.delete()
        messages.success(request, "Producto eliminado del carrito.")
    else:
        messages.error(request, "Producto no encontrado.")
    return redirect('ver_carrito')


@login_required
def procesar_pago(request):
    carrito = request.user.carrito
    items = carrito.items.all()

    if not items:
        messages.error(request, "No hay productos en el carrito.")
        return redirect('ver_carrito')

    compra = Compra.objects.create(usuario=request.user)

    for item in items:
        ItemCompra.objects.create(
            compra=compra,
            nombre=item.producto.nombre,
            precio=item.precio,
            cantidad=item.cantidad,
            subtotal=item.subtotal()
        )

    items.delete()
    messages.success(request, "Pago procesado con éxito. Tu compra ha sido registrada.")
    return redirect('historial_compras')
