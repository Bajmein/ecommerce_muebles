import os
import django
from muebles.models import Categoria, Producto


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_muebles.settings')
django.setup()

CATEGORIAS = {
    "Sillas": [
        {"nombre": "Silla de Madera Clasica", "precio": 120.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla de Madera Moderna", "precio": 125.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla de Madera Rustica", "precio": 130.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla de Madera Vintage", "precio": 135.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla Tapizada Elegante", "precio": 150.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla Tapizada Casual", "precio": 140.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla Tapizada Clasica", "precio": 145.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla Tapizada Sofisticada", "precio": 155.000, "imagen": "https://via.placeholder.com/120"},
    ],
    "Mesas": [
        {"nombre": "Mesa Redonda Clasica", "precio": 200.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa Redonda Moderna", "precio": 210.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa Redonda Rustica", "precio": 220.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa Redonda Elegante", "precio": 230.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa Extensible Compacta", "precio": 300.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa Extensible Versatil", "precio": 310.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa Extensible Moderna", "precio": 320.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa Extensible Elegante", "precio": 330.000, "imagen": "https://via.placeholder.com/120"},
    ],
    "Estanterias": [
        {"nombre": "Estanteria de Madera Clasica", "precio": 180.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria de Madera Moderna", "precio": 190.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria de Madera Rustica", "precio": 200.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria de Madera Elegante", "precio": 210.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria Metalica Clasica", "precio": 220.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria Metalica Moderna", "precio": 230.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria Metalica Rustica", "precio": 240.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria Metalica Elegante", "precio": 250.000, "imagen": "https://via.placeholder.com/120"},
    ],
}

DIMENSIONES = {
    "Sillas": "45x45x90 cm",
    "Mesas": "120x75x75 cm",
    "Estanterias": "80x30x180 cm",
}

DESCRIPCION_TEMPLATE = ("Este producto destaca por su diseño {adjetivo} y su calidad superior. Perfecto para cualquier "
                        "entorno.")

ADJETIVOS = ["clasico", "moderno", "rustico", "elegante", "versatil", "sofisticado"]


def cargar_datos():
    for categoria_nombre, productos in CATEGORIAS.items():
        # Crear o obtener la categoría
        categoria, _ = Categoria.objects.get_or_create(
            nombre=categoria_nombre,
            defaults={"descripcion": f"Productos de la categoría {categoria_nombre.lower()}."}
        )

        for producto in productos:
            # Generar descripción aleatoria
            adjetivo = ADJETIVOS[len(producto["nombre"]) % len(ADJETIVOS)]
            descripcion = DESCRIPCION_TEMPLATE.format(adjetivo=adjetivo)

            # Crear el producto
            Producto.objects.get_or_create(
                nombre=producto["nombre"],
                defaults={
                    "precio": producto["precio"],
                    "imagen": producto["imagen"],
                    "descripcion": descripcion,
                    "dimensiones": DIMENSIONES[categoria_nombre],
                    "categoria": categoria,
                }
            )


cargar_datos()
print("Datos cargados exitosamente.")
