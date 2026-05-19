"""
procesador.py
=============
Clase principal para cargar archivos DICOM, extraer metadatos,
analizar intensidad de píxeles y procesar imágenes médicas con OpenCV.

Integrantes:
    - Miguel Angel Toro
    - Stefania Concha Caceres
"""

import os
import pydicom
import numpy as np
import pandas as pd
import cv2


class ProcesadorDICOM:
    """
    Clase que encapsula toda la lógica para procesar archivos DICOM.

    Atributos:
        ruta      : carpeta donde están los archivos .dcm
        archivos  : lista de datasets cargados con pydicom
        dataframe : DataFrame con los metadatos extraídos
    """

    def __init__(self, ruta):
        self.ruta = ruta
        self.archivos = []
        self.dataframe = None

    # ------------------------------------------------------------------
    # 1. Carga de archivos
    # ------------------------------------------------------------------

    def cargar_archivos(self):
        """
        Escanea la carpeta, carga todos los archivos DICOM válidos
        y los guarda en self.archivos.
        """
        encontrados = 0
        for nombre in os.listdir(self.ruta):
            ruta_archivo = os.path.join(self.ruta, nombre)
            try:
                dataset = pydicom.dcmread(ruta_archivo)
                self.archivos.append(dataset)
                encontrados += 1
                print(f"  Cargado: {nombre}")
            except Exception:
                # El archivo no es un DICOM válido, se omite
                print(f"  Omitido (no es DICOM): {nombre}")

        print(f"\n  Total cargados: {encontrados} archivo(s)\n")

    # ------------------------------------------------------------------
    # 2. Extracción de metadatos
    # ------------------------------------------------------------------

    def extraer_metadatos(self):
        """
        Extrae los tags DICOM de cada archivo cargado y construye
        un DataFrame donde cada fila es un archivo y cada columna un tag.
        """

        def obtener_tag(dataset, tag):
            # Retorna el valor del tag o 'N/A' si no existe (anonimizado)
            return str(getattr(dataset, tag, "N/A"))

        filas = []
        for ds in self.archivos:
            fila = {
                "PatientID"          : obtener_tag(ds, "PatientID"),
                "PatientName"        : obtener_tag(ds, "PatientName"),
                "StudyInstanceUID"   : obtener_tag(ds, "StudyInstanceUID"),
                "StudyDescription"   : obtener_tag(ds, "StudyDescription"),
                "StudyDate"          : obtener_tag(ds, "StudyDate"),
                "Modality"           : obtener_tag(ds, "Modality"),
                "Rows"               : obtener_tag(ds, "Rows"),
                "Columns"            : obtener_tag(ds, "Columns"),
            }
            filas.append(fila)

        self.dataframe = pd.DataFrame(filas)
        print("  Metadatos extraídos correctamente.")
        print(self.dataframe.to_string())
        print()