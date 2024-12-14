import os
import django
from muebles.models import Categoria, Producto


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_muebles.settings')
django.setup()

CATEGORIAS = {
    "Sillas": [
        {"nombre": "Silla de madera clasica", "precio": 120.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla de madera moderna", "precio": 125.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla de madera rustica", "precio": 130.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla de madera vintage", "precio": 135.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla tapizada elegante", "precio": 150.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla tapizada casual", "precio": 140.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla tapizada clasica", "precio": 145.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Silla tapizada sofisticada", "precio": 155.000, "imagen": "https://via.placeholder.com/120"},
    ],
    "Mesas": [
        {"nombre": "Mesa redonda clasica", "precio": 200.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa redonda moderna", "precio": 210.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa redonda rustica", "precio": 220.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa redonda elegante", "precio": 230.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa extensible compacta", "precio": 300.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa extensible versatil", "precio": 310.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa extensible moderna", "precio": 320.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Mesa extensible elegante", "precio": 330.000, "imagen": "https://via.placeholder.com/120"},
    ],
    "Estanterias": [
        {"nombre": "Estanteria de madera clasica", "precio": 180.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria de madera moderna", "precio": 190.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria de madera rustica", "precio": 200.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria de madera elegante", "precio": 210.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria metalica clasica", "precio": 220.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria metalica moderna", "precio": 230.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria metalica rustica", "precio": 240.000, "imagen": "https://via.placeholder.com/120"},
        {"nombre": "Estanteria metalica elegante", "precio": 250.000, "imagen": "https://via.placeholder.com/120"},
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
        categoria, _ = Categoria.objects.get_or_create(
            nombre=categoria_nombre,
            defaults={"descripcion": f"Productos de la categoría {categoria_nombre.lower()}."}
        )

        for producto in productos:
            adjetivo = ADJETIVOS[len(producto["nombre"]) % len(ADJETIVOS)]
            descripcion = DESCRIPCION_TEMPLATE.format(adjetivo=adjetivo)

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
