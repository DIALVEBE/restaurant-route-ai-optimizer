from math import (
    radians,
    sin,
    cos,
    sqrt,
    atan2
)

import random


class RouteOptimizer:

    def __init__(
        self,
        restaurantes
    ):

        self.restaurantes = restaurantes

        self.random = random.Random(42)


    # =========================
    # Distancia entre 2 puntos
    # =========================
    def distancia(
        self,
        restaurante_a,
        restaurante_b
    ):

        lat1 = radians(
            restaurante_a["lat"]
        )

        lng1 = radians(
            restaurante_a["lng"]
        )

        lat2 = radians(
            restaurante_b["lat"]
        )

        lng2 = radians(
            restaurante_b["lng"]
        )


        # =========================
        # Fórmula Haversine
        # =========================

        diferencia_lat = (
            lat2 - lat1
        )

        diferencia_lng = (
            lng2 - lng1
        )


        a = (
            sin(
                diferencia_lat / 2
            ) ** 2
            +
            cos(lat1)
            * cos(lat2)
            * sin(
                diferencia_lng / 2
            ) ** 2
        )


        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a)
        )


        # Radio aproximado
        # de la Tierra
        radio = 6371


        return radio * c


    # =========================
    # Crear ruta aleatoria
    # =========================
    def crear_ruta(self):

        cantidad = len(
            self.restaurantes
        )


        # Restaurante 0 queda fijo
        resto = list(
            range(1, cantidad)
        )


        self.random.shuffle(
            resto
        )


        return [0] + resto


    # =========================
    # Calcular distancia total
    # =========================
    def distancia_ruta(
        self,
        ruta
    ):

        total = 0


        # Recorrer la ruta
        for i in range(
            len(ruta) - 1
        ):

            actual = (
                self.restaurantes
                .iloc[ruta[i]]
            )

            siguiente = (
                self.restaurantes
                .iloc[ruta[i + 1]]
            )


            total += self.distancia(
                actual,
                siguiente
            )


        # =========================
        # Regresar al inicio
        # =========================

        ultimo = (
            self.restaurantes
            .iloc[ruta[-1]]
        )

        primero = (
            self.restaurantes
            .iloc[ruta[0]]
        )


        total += self.distancia(
            ultimo,
            primero
        )


        return total


    # =========================
    # Crear vecino
    # =========================
    def crear_vecino(
        self,
        ruta
    ):

        vecino = ruta.copy()


        # Elegir 2 posiciones
        # excepto la posición 0
        i, j = self.random.sample(
            range(1, len(ruta)),
            2
        )


        # Intercambiar
        vecino[i], vecino[j] = (
            vecino[j],
            vecino[i]
        )


        return vecino


    # =========================
    # Hill Climbing
    # =========================
    def optimizar(
        self,
        ruta
    ):

        ruta_actual = ruta.copy()

        distancia_actual = (
            self.distancia_ruta(
                ruta_actual
            )
        )


        mejoras = 0


        # Probar 5000 vecinos
        for iteracion in range(
            1,
            5001
        ):

            vecino = (
                self.crear_vecino(
                    ruta_actual
                )
            )


            distancia_vecino = (
                self.distancia_ruta(
                    vecino
                )
            )


            # =========================
            # ¿Es mejor?
            # =========================

            if (
                distancia_vecino
                < distancia_actual
            ):

                ruta_actual = vecino

                distancia_actual = (
                    distancia_vecino
                )

                mejoras += 1


                print(
                    f"Iteración "
                    f"{iteracion:4} | "
                    f"{distancia_actual:.2f} km "
                    f"✅"
                )


        return (
            ruta_actual,
            distancia_actual,
            mejoras
        )
