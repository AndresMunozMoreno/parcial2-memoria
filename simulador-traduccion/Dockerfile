# ==============================================================
# Proyecto: Simulador de Administración de Memoria
# Autor: Andrés Felipe Muñoz Moreno
# Asignatura: Sistemas Operativos - Universidad del Valle
# Archivo: Dockerfile (Simulador de Traducción de Direcciones)
#
# Descripción:
# Construye una imagen ligera con Python 3.12 que ejecuta el
# menú interactivo del simulador de traducción de direcciones
# virtuales a físicas (paginación de un nivel).
# ==============================================================

FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero requirements.txt para aprovechar el cache de
# capas de Docker: si el código cambia pero las dependencias no,
# no se reinstalan innecesariamente.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente y los archivos de entrada de ejemplo
COPY src/ ./src/
COPY entradas/ ./entradas/

# Nos ubicamos en src/ para que los imports relativos (core, models, ui)
# se resuelvan igual que en desarrollo local
WORKDIR /app/src

# Ejecutamos el menú interactivo como módulo, igual que en local
CMD ["python3", "-m", "ui.main"]