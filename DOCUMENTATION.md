# Documentación del Trabajo Práctico: Editor de Imágenes con Qwen

## Descripción de la Aplicación
Se desarrolló una interfaz web interactiva usando Streamlit que funciona como un centro de edición de imágenes. Los usuarios pueden cargar una foto y generar múltiples ángulos usando el modelo Qwen-Edit-2509-Multiple-Angles de Hugging Face. La app incluye:
- Modo oscuro y claro.
- Barra lateral para herramientas (carga de imagen, prompt, fuerza de edición).
- Panel principal para previsualización de la imagen original y editada.

## Flujo de Desarrollo
1. **Desarrollo Local**: Se creó el código en `app.py` usando Streamlit.
2. **Dependencias**: Se listaron en `requirements.txt`.
3. **Contenerización**: Se creó un `Dockerfile` para empaquetar la app.
4. **Orquestación**: Se usó `docker-compose.yml` para definir servicios.
5. **CI/CD**: Se configuró GitHub Actions para build y push automático a Docker Hub.
6. **Despliegue**: Se ejecutó en contenedores y se probó en Play with Docker con templates.

## Instalación y Configuración
### Prerrequisitos
- Docker instalado.
- Cuenta en Docker Hub (usuario: rodyuzuriaga).
- Git y GitHub para repositorio.

### Pasos de Instalación
1. Clonar el repositorio:
   ```
   git clone https://github.com/usuario/repo.git
   cd repo
   ```

2. Construir la imagen Docker (esto descarga los modelos ~4GB):
   ```
   docker build -t rodyuzuriaga/st-app:latest .
   ```

3. Ejecutar localmente:
   ```
   docker run -d -p 5000:5000 --name image-editor rodyuzuriaga/st-app:latest
   ```

4. Acceder a http://localhost:5000

## Comandos Usados
### Docker Básicos
- Ver imágenes: `docker images`
- Ver contenedores: `docker ps` / `docker ps -a`
- Ejecutar contenedor: `docker run -d -p 8501:8501 --name app-streamlit rodyuzuriaga/st-app:latest`

### Docker Hub
- Login: `docker login -u rodyuzuriaga`
- Tag: `docker tag st-app rodyuzuriaga/st-app:latest`
- Push: `docker push rodyuzuriaga/st-app:latest`
- Pull: `docker pull rodyuzuriaga/st-app:latest`

### Docker Compose
- Desplegar con compose: `docker stack deploy -c docker-compose.yml myapp`
- (Para Swarm: inicializar swarm primero con `docker swarm init`)

### GitHub Actions
- El workflow se activa en push a main.
- Requiere secrets: DOCKER_USERNAME y DOCKER_PASSWORD en el repo de GitHub.

## Uso de Templates en Play with Docker
- **3 Managers + 2 Workers**: Ideal para resiliencia. Desplegar con `docker stack deploy` para replicación.
- Ejecutar en https://labs.play-with-docker.com/

## Notas Adicionales
- El modelo Qwen requiere GPU para rendimiento óptimo; en CPU puede ser lento.
- Para producción, optimizar el Dockerfile y usar volumes para modelos.