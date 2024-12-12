from django.urls import path
from muebles import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('historial_compras/', views.historial_compras, name='historial_compras'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/<str:categoria>/', views.listar_muebles_por_categoria, name='listar_muebles_por_categoria'),
    path('categorias/<str:categoria>/<str:mueble_nombre>/', views.detalle_mueble_por_categoria,
         name='detalle_mueble_por_categoria'),
    path('buscar/', views.buscar_muebles, name='buscar_muebles'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<str:categoria>/<str:producto_nombre>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
]
