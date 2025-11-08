# Infinite Axis - Background Removal AI

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

Aplicación web para eliminar fondos de imágenes automáticamente usando IA con la librería Rembg.

## Características

- **Eliminación automática de fondos**: Procesa imágenes en 2-5 segundos usando rembg con modelo U2-Net
- **Validación de archivos**: Solo acepta PNG, JPG y JPEG con validación de tipos
- **Optimización de memoria inteligente**: Algoritmos matemáticos para minimizar uso de RAM (< 200MB)
- **Redimensionamiento automático**: Imágenes grandes (>1024px) se optimizan manteniendo proporción
- **Compresión adaptativa**: Usa ratios de compresión matemáticos para eficiencia máxima
- **Monitoreo de memoria**: Seguimiento en tiempo real del uso de recursos
- **Limpieza automática**: Liberación forzada de memoria y garbage collection
- **Preview instantáneo**: Visualiza tu imagen inmediatamente al seleccionarla
- **Información de calidad**: Muestra resolución, formato, tamaño y si fue redimensionada
- **Interfaz moderna**: Diseño responsivo con modo oscuro/claro
- **Descarga simple**: Exporta imágenes PNG con fondo transparente
- **Indicadores de progreso**: Logs detallados del proceso de eliminación de fondo
- **Docker Ready**: Dockerfile y configuración completa para despliegue
- **CI/CD Automatizado**: GitHub Actions para publicación automática en Docker Hub

## Requisitos Previos

- Docker y Docker Compose
- Python 3.9+ (para desarrollo local)
- Git

## Despliegue con Docker

### Desde Docker Hub (Recomendado)

```bash
# Descargar imagen desde Docker Hub
docker pull rodyuzuriaga/infinite-axis:latest

# Ejecutar contenedor
docker run -d -p 5000:5000 --name infinite-axis rodyuzuriaga/infinite-axis:latest
```

Acceder a la aplicación en: http://localhost:5000

### Construir localmente

```bash
# Clonar repositorio
git clone https://github.com/rodyuzuriaga/Infinite-Axis.git
cd Infinite-Axis

# Construir imagen Docker
docker build -t infinite-axis .

# Ejecutar contenedor
docker run -d -p 5000:5000 --name infinite-axis infinite-axis
```

### Usando Docker Compose

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down
```

## Desarrollo Local

### Instalación de dependencias

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar servidor de desarrollo

```bash
python app.py
```

La aplicación estará disponible en http://localhost:5000

## Uso de la Aplicación

1. **Cargar imagen**: Haz clic en el área de carga o arrastra una imagen PNG/JPG/JPEG
2. **Validación automática**: La app valida el tipo de archivo y muestra información de calidad
3. **Redimensionamiento**: Imágenes grandes (>2048px) se redimensionan automáticamente manteniendo proporción
4. **Remover fondo**: Presiona el botón "Remover Fondo" y observa el progreso en los logs
5. **Descargar resultado**: Haz clic en el botón de descarga para obtener la imagen PNG transparente
6. **Reiniciar**: Usa el botón "Reiniciar" para limpiar y procesar una nueva imagen

### Límites y Validaciones

- **Formatos soportados**: PNG, JPG, JPEG
- **Tamaño máximo**: Sin límite estricto, optimización automática para cualquier tamaño
- **Optimización inteligente**: Imágenes >1024px se comprimen matemáticamente manteniendo calidad
- **Procesamiento**: Algoritmos adaptativos que ajustan chunk size según memoria disponible
- **Memoria**: Optimizado para <200MB RAM (adecuado para contenedores con 512MB)
- **Compresión**: Ratios matemáticos para máxima eficiencia sin pérdida perceptible de calidad

## Estructura del Proyecto

```
Infinite-Axis/
├── app.py                 # Servidor Flask con API de background removal
├── front.html            # Interfaz de usuario moderna
├── requirements.txt      # Dependencias Python
├── Dockerfile           # Configuración Docker
├── docker-compose.yml   # Orquestación de contenedores
├── .github/
│   └── workflows/
│       └── docker-publish.yml  # CI/CD GitHub Actions
└── generated/           # Carpeta temporal para imágenes procesadas
```

## Tecnologías Utilizadas

- **Backend**: Flask, Rembg, Pillow
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **IA**: Modelo U2-Net para segmentación de imágenes
- **Containerización**: Docker
- **CI/CD**: GitHub Actions

## Despliegue en Play with Docker

1. Acceder a https://labs.play-with-docker.com/
2. Crear nueva instancia
3. Ejecutar comandos:

```bash
git clone https://github.com/rodyuzuriaga/Infinite-Axis.git
cd Infinite-Axis
docker build -t infinite-axis .
docker run -d -p 5000:5000 infinite-axis
```

4. Hacer clic en el botón "OPEN PORT" e ingresar `5000`

## CI/CD y Docker Hub

Este proyecto está configurado con GitHub Actions para publicación automática en Docker Hub:

- **Push a main**: Automáticamente construye y publica la imagen como `latest`
- **Tags**: Las versiones etiquetadas se publican con su número de versión
- **Secretos configurados**: 
  - `DOCKERHUB_USERNAME`: Usuario de Docker Hub
  - `DOCKERHUB_TOKEN`: Token de acceso de Docker Hub

La imagen está disponible públicamente en: https://hub.docker.com/r/rodyuzuriaga/infinite-axis

## Autor

**Rody Uzuriaga**
- GitHub: [@rodyuzuriaga](https://github.com/rodyuzuriaga)
- Docker Hub: [rodyuzuriaga](https://hub.docker.com/u/rodyuzuriaga)

## Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.