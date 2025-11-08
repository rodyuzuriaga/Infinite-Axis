# Usar imagen base de Python
FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# PRE-DESCARGAR MODELO REMBG (176 MB) - Se descarga UNA VEZ durante build
RUN python -c "from rembg import remove; from PIL import Image; import io; remove(Image.new('RGB', (100, 100)))"

# Copiar código
COPY app.py .
COPY front.html .

# Crear directorio para imágenes generadas
RUN mkdir -p generated

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar
CMD ["python", "-u", "app.py"]