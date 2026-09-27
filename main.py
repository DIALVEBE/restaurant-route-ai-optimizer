from rich.console import Console
from rich.table import Table

from restaurant_data import RestaurantData
from route_optimizer import RouteOptimizer


console = Console()


# =========================
# 1. Cargar restaurantes
# =========================

console.rule(
    "[bold]1. Dataset"
)


datos = RestaurantData()


restaurantes = datos.cargar(
    cantidad=15
)


# =========================
# Mostrar restaurantes
# =========================

tabla = Table(
    title="Restaurantes seleccionados"
)


tabla.add_column("#")
tabla.add_column("Restaurante")
tabla.add_column("Dirección")


for i, restaurante in (
    restaurantes.iterrows()
):

    tabla.add_row(

        str(i),

        restaurante["name"],

        restaurante[
            "full_address"
        ]
    )


console.print(tabla)


# =========================
# 2. Crear optimizador
# =========================

optimizador = RouteOptimizer(
    restaurantes
)


# =========================
# 3. Ruta inicial
# =========================

console.rule(
    "[bold]2. Ruta inicial"
)


ruta_inicial = (
    optimizador.crear_ruta()
)


distancia_inicial = (
    optimizador.distancia_ruta(
        ruta_inicial
    )
)


console.print(
    f"\nRuta:"
)

console.print(
    " → ".join(
        str(i)
        for i in ruta_inicial
    )
)


console.print(
    f"\nDistancia inicial: "
    f"[red]"
    f"{distancia_inicial:.2f} km"
    f"[/red]"
)


# =========================
# 4. Optimizar
# =========================

console.rule(
    "[bold]3. Hill Climbing"
)


(
    mejor_ruta,
    distancia_final,
    mejoras
) = optimizador.optimizar(
    ruta_inicial
)


# =========================
# 5. Resultado
# =========================

console.rule(
    "[bold green]"
    "4. Resultado"
)


porcentaje = (
    (
        distancia_inicial
        - distancia_final
    )
    / distancia_inicial
    * 100
)


console.print(
    f"\nDistancia inicial: "
    f"[red]"
    f"{distancia_inicial:.2f} km"
    f"[/red]"
)


console.print(
    f"Distancia optimizada: "
    f"[green]"
    f"{distancia_final:.2f} km"
    f"[/green]"
)


console.print(
    f"Mejora: "
    f"[cyan]"
    f"{porcentaje:.2f}%"
    f"[/cyan]"
)


console.print(
    f"Mejoras aceptadas: "
    f"{mejoras}"
)


# =========================
# Mejor ruta
# =========================

console.print(
    "\n[bold]"
    "Ruta optimizada:"
    "[/bold]"
)


console.print(
    " → ".join(
        str(i)
        for i in mejor_ruta
    )
)
