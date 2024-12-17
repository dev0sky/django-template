# Main image project based on Python 3.12
FROM python:3.11

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y gettext libpq-dev

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Crear el directorio principal del proyecto y establecer el directorio de trabajo
WORKDIR /api

# Copiar el archivo de requisitos del proyecto
COPY requirements.txt ./

# Actualizar pip y instalar las dependencias
RUN python -m pip install --upgrade pip && pip install wheel
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copiar el directorio del proyecto al contenedor
COPY . .