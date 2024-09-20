# Usamos una imagen de Python oficial y liviana
FROM python:3.9-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo requirements.txt
COPY requirements.txt requirements.txt

# Instalamos las dependencias listadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código del bot al contenedor (opcional si no usas volúmenes para el código)
# COPY telegram_bot.py telegram_bot.py

# Comando por defecto para ejecutar el bot (esto puede ser configurado en docker-compose.yml)
CMD ["python", "telegram_bot.py"]
