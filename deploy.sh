#!/bin/bash

# 🎨 Script de Despliegue Rápido - Infinite Axis
# Para usar en Play with Docker

echo "🚀 Infinite Axis - Despliegue Automático"
echo "=========================================="

# Clonar repositorio
echo "📦 Clonando repositorio..."
git clone https://github.com/rodyuzuriaga/Infinite-Axis.git
cd Infinite-Axis

# Construir imagen
echo "🔨 Construyendo imagen Docker..."
docker build -t infinite-axis .

# Ejecutar contenedor
echo "▶️  Ejecutando contenedor..."
docker run -d -p 5000:5000 --name infinite-axis infinite-axis

# Esperar 3 segundos
sleep 3

# Verificar estado
echo "✅ Verificando estado..."
docker ps | grep infinite-axis

echo ""
echo "🎉 ¡Despliegue completado!"
echo "📍 Accede en: http://localhost:5000"
echo "📋 Ver logs: docker logs -f infinite-axis"
echo "🛑 Detener: docker stop infinite-axis"
