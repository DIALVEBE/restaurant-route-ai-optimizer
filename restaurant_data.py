from pathlib import Path

import kagglehub
import pandas as pd


class RestaurantData:

    def __init__(self):
        self.dataset = (
            "ahmedshahriarsakib/"
            "uber-eats-usa-restaurants-menus"
        )


    # =========================
    # Descargar dataset
    # =========================
    def descargar(self):

        print("Descargando dataset...")

        path = kagglehub.dataset_download(
            self.dataset
        )

        print("Dataset disponible en:")
        print(path)

        return Path(path)


    # =========================
    # Cargar restaurantes
    # =========================
    def cargar(
        self,
        cantidad=15,
        zip_code=None
    ):

        path = self.descargar()

        archivo = (
            path / "restaurants.csv"
        )


        # =========================
        # Leer CSV
        # =========================
        df = pd.read_csv(
            archivo,
            dtype={
                "zip_code": "string"
            }
        )


        # =========================
        # Solo columnas necesarias
        # =========================
        df = df[
            [
                "id",
                "name",
                "full_address",
                "zip_code",
                "lat",
                "lng"
            ]
        ]


        # =========================
        # Eliminar datos incompletos
        # =========================
        df = df.dropna(
            subset=[
                "name",
                "zip_code",
                "lat",
                "lng"
            ]
        )


        # =========================
        # Eliminar coordenadas
        # repetidas
        # =========================
        df = df.drop_duplicates(
            subset=[
                "lat",
                "lng"
            ]
        )


        # =========================
        # Elegir zona
        # =========================
        if zip_code is None:

            conteos = (
                df["zip_code"]
                .value_counts()
            )


            # Buscar ZIP con suficientes
            # restaurantes
            zonas = conteos[
                conteos >= cantidad
            ]


            if zonas.empty:

                raise ValueError(
                    "No existe un ZIP con "
                    "suficientes restaurantes."
                )


            # Escoger el ZIP con más
            # restaurantes
            zip_code = zonas.index[0]


        print()
        print(
            f"ZIP seleccionado: "
            f"{zip_code}"
        )


        # =========================
        # Filtrar zona
        # =========================
        zona = df[
            df["zip_code"]
            == str(zip_code)
        ]


        # =========================
        # Seleccionar restaurantes
        # =========================
        restaurantes = zona.sample(
            n=cantidad,
            random_state=42
        )


        restaurantes = (
            restaurantes
            .reset_index(drop=True)
        )


        return restaurantes
