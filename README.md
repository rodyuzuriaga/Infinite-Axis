# 🎨 Infinite Axis - Generador de Ángulos de Imagen con IA

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

Aplicación web para generar múltiples ángulos y perspectivas de imágenes usando controles de cámara profesionales.

## 🚀 Características

- 🎛️ **Controles de Cámara Profesionales**: Sliders para rotar, acercar y cambiar ángulo vertical
- 🎨 **Interfaz Moderna**: Diseño oscuro/claro con Tailwind CSS
- 🐳 **Docker Ready**: Dockerfile y docker-compose.yml incluidos
- ⚡ **CI/CD Automatizado**: GitHub Actions para Docker Hub
- 🌐 **Multilenguaje**: Interfaz en español

## 📋 Requisitos Previos

- Docker y Docker Compose
- Python 3.9+ (para desarrollo local)
- Git

## 🐳 Despliegue Rápido con Docker

### Opción 1: Docker Hub (Recomendado)

```bash
# Descargar y ejecutar desde Docker Hub
docker pull rodyuzuriaga/infinite-axis:latest
docker run -d -p 5000:5000 --name infinite-axis rodyuzuriaga/infinite-axis:latest
```

### Opción 2: Construir localmente

```bash
# Clonar repositorio
git clone https://github.com/rodyuzuriaga/Infinite-Axis.git
cd Infinite-Axis

# Construir imagen
docker build -t infinite-axis .

# Ejecutar contenedor
docker run -d -p 5000:5000 --name infinite-axis infinite-axis
```

## 🚢 Despliegue en Play with Docker

1. Ir a https://labs.play-with-docker.com/
2. Clonar repositorio:
   ```bash
   git clone https://github.com/rodyuzuriaga/Infinite-Axis.git
   cd Infinite-Axis
   ```
3. Construir y ejecutar:
   ```bash
   docker build -t infinite-axis .
   docker run -d -p 5000:5000 --name infinite-axis infinite-axis
   ```
4. Click en "OPEN PORT" → Ingresar `5000`

## 👨‍💻 Autor

**Rody Uzuriaga**
- GitHub: [@rodyuzuriaga](https://github.com/rodyuzuriaga)

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!