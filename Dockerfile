# Usar imagen base de Python
FROM python:3.11-slim

# Build version: 2025-11-07-v3
# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app.py .
COPY front.html .

# Crear directorio para imágenes generadas
RUN mkdir -p generated

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar
CMD ["python", "-u", "app.py"]