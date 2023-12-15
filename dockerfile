# Usa la imagen base de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia el contenido actual del directorio al contenedor en /app
COPY . .

# Expone el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación Flask
CMD ["python", "app.py"]
