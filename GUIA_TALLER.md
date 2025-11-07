# 📘 GUÍA COMPLETA - TALLER PRÁCTICO DOCKER

## 🎯 Objetivo
Desplegar **Infinite Axis** en Play with Docker y automatizar publicación en Docker Hub.

---

## ✅ PARTE 1: CONFIGURAR DOCKER HUB Y CI/CD

### Paso 1.1: Crear Token en Docker Hub

1. Ir a: https://hub.docker.com/settings/security
2. Click en **"New Access Token"**
3. Configurar:
   - **Description**: `github-actions-infinite-axis`
   - **Access permissions**: ☑️ Read, Write, Delete
4. Click **"Generate"**
5. **⚠️ COPIAR EL TOKEN INMEDIATAMENTE** (solo se muestra una vez)

### Paso 1.2: Agregar Secrets en GitHub

1. Ir a: https://github.com/rodyuzuriaga/Infinite-Axis/settings/secrets/actions
2. Click **"New repository secret"**
3. Agregar primer secret:
   - **Name**: `DOCKER_USERNAME`
   - **Secret**: `rodyuzuriaga`
   - Click "Add secret"
4. Agregar segundo secret:
   - **Name**: `DOCKER_PASSWORD`
   - **Secret**: `[PEGAR_TOKEN_DE_DOCKER_HUB]`
   - Click "Add secret"

### Paso 1.3: Verificar CI/CD Automático

1. Ir a: https://github.com/rodyuzuriaga/Infinite-Axis/actions
2. Deberías ver un workflow corriendo
3. Esperar que termine (círculo verde ✅)
4. Ir a Docker Hub: https://hub.docker.com/r/rodyuzuriaga/infinite-axis
5. Deberías ver la imagen publicada con tag `latest`

---

## ✅ PARTE 2: DESPLEGAR EN PLAY WITH DOCKER

### Paso 2.1: Acceder a Play with Docker

1. Ir a: https://labs.play-with-docker.com/
2. Click **"Login"** (usar cuenta Docker Hub)
3. Click **"Start"**
4. Click **"+ ADD NEW INSTANCE"**

### Paso 2.2: Listar Imágenes y Contenedores (Comandos del Taller)

```bash
# Ver imágenes disponibles (inicialmente vacío)
docker images

# Ver contenedores en ejecución (inicialmente vacío)
docker ps

# Ver todos los contenedores (activos e inactivos)
docker ps -a
```

### Paso 2.3: Probar con NGINX (Ejemplo del Taller)

```bash
# Ejecutar nginx (se descarga automáticamente)
docker run -d -p 8080:80 --name mi-nginx nginx

# Verificar que está corriendo
docker ps

# Ver logs de nginx
docker logs mi-nginx

# Detener nginx
docker stop mi-nginx

# Eliminar nginx
docker rm mi-nginx

# Verificar que se eliminó
docker ps -a
```

**Desglose del comando `docker run`:**
- `docker run`: Crea y ejecuta un contenedor
- `-d`: Detached (segundo plano)
- `-p 8080:80`: Mapeo de puertos (host:contenedor)
- `--name mi-nginx`: Nombre personalizado
- `nginx`: Imagen a usar

### Paso 2.4: Desplegar Infinite Axis desde GitHub

```bash
# Clonar repositorio
git clone https://github.com/rodyuzuriaga/Infinite-Axis.git

# Entrar al directorio
cd Infinite-Axis

# Ver archivos
ls -la

# Ver contenido del Dockerfile
cat Dockerfile

# Ver dependencias
cat requirements.txt
```

### Paso 2.5: Construir Imagen Docker

```bash
# Construir imagen (tarda ~2-3 minutos)
docker build -t infinite-axis .

# Verificar que se creó la imagen
docker images

# Deberías ver:
# REPOSITORY       TAG      IMAGE ID       CREATED         SIZE
# infinite-axis    latest   xxxxxxxxxxxx   X seconds ago   ~500MB
```

### Paso 2.6: Ejecutar Contenedor

```bash
# Ejecutar contenedor
docker run -d -p 5000:5000 --name infinite-axis infinite-axis

# Verificar que está corriendo
docker ps

# Ver logs en tiempo real
docker logs -f infinite-axis

# Presionar CTRL+C para salir de logs
```

### Paso 2.7: Acceder a la Aplicación

1. En Play with Docker, aparecerá un botón **"5000"** en la parte superior
2. Click en **"5000"** o en **"OPEN PORT"** → ingresar `5000`
3. Se abrirá Infinite Axis en nueva pestaña
4. Probar:
   - Subir una imagen
   - Ajustar sliders
   - Generar ángulos
   - Descargar resultado

---

## ✅ PARTE 3: GESTIONAR CONTENEDORES

### Comandos de Gestión

```bash
# Ver logs completos
docker logs infinite-axis

# Ver logs en tiempo real
docker logs -f infinite-axis

# Ver estadísticas de recursos
docker stats infinite-axis

# Pausar contenedor
docker pause infinite-axis

# Reanudar contenedor
docker unpause infinite-axis

# Reiniciar contenedor
docker restart infinite-axis

# Detener contenedor
docker stop infinite-axis

# Iniciar contenedor detenido
docker start infinite-axis

# Eliminar contenedor (debe estar detenido)
docker stop infinite-axis
docker rm infinite-axis

# Forzar eliminación (sin detener)
docker rm -f infinite-axis

# Verificar eliminación
docker ps -a
```

---

## ✅ PARTE 4: DESCARGAR DESDE DOCKER HUB

### Método Alternativo: Pull desde Docker Hub

```bash
# Si ya publicaste en Docker Hub con GitHub Actions:
docker pull rodyuzuriaga/infinite-axis:latest

# Ejecutar directamente
docker run -d -p 5000:5000 --name infinite-axis rodyuzuriaga/infinite-axis:latest

# Verificar
docker ps
```

---

## ✅ PARTE 5: PUBLICAR EN DOCKER HUB MANUALMENTE

### Opción Manual (si no usaste GitHub Actions)

```bash
# 1. Iniciar sesión en Docker Hub
docker login -u rodyuzuriaga
# Ingresar contraseña (o token)

# 2. Etiquetar imagen
docker tag infinite-axis rodyuzuriaga/infinite-axis:latest

# 3. Publicar imagen
docker push rodyuzuriaga/infinite-axis:latest

# 4. Verificar en: https://hub.docker.com/r/rodyuzuriaga/infinite-axis
```

---

## ✅ PARTE 6: LIMPIEZA Y MANTENIMIENTO

### Comandos de Limpieza

```bash
# Eliminar contenedor
docker rm -f infinite-axis

# Eliminar imagen local
docker rmi infinite-axis

# Eliminar imagen de Docker Hub
docker rmi rodyuzuriaga/infinite-axis:latest

# Eliminar todos los contenedores parados
docker container prune

# Eliminar todas las imágenes sin usar
docker image prune -a

# Limpieza completa (contenedores, imágenes, redes, volúmenes)
docker system prune -a --volumes

# Ver espacio ocupado
docker system df
```

---

## ✅ PARTE 7: DOCKER COMPOSE (ALTERNATIVA)

### Opción con Docker Compose

```bash
# Si tienes docker-compose.yml en el repositorio:
cd Infinite-Axis

# Ejecutar con compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reconstruir y ejecutar
docker-compose up -d --build
```

---

## 📊 COMPARACIÓN: Docker Hub CI/CD vs Manual

| Método | GitHub Actions (Automático) | Manual (Play with Docker) |
|--------|----------------------------|---------------------------|
| **Trigger** | Push a GitHub | Comando manual |
| **Build** | En GitHub Runners | En Play with Docker |
| **Publish** | Automático a Docker Hub | Manual con `docker push` |
| **Tiempo** | ~5 minutos | ~2 minutos |
| **Ventaja** | Automatizado, reproducible | Control total, depuración |

---

## 🎓 CONCEPTOS CLAVE DEL TALLER

### 1. Imágenes vs Contenedores
- **Imagen**: Plantilla inmutable (como una clase)
- **Contenedor**: Instancia en ejecución (como un objeto)

### 2. Mapeo de Puertos
- `-p 5000:5000`: puerto_host:puerto_contenedor
- Permite acceder desde navegador al puerto del contenedor

### 3. Modos de Ejecución
- `-d`: Detached (segundo plano)
- Sin `-d`: Attached (se ven logs en terminal)

### 4. Nombres de Contenedores
- `--name mi-contenedor`: Nombre personalizado
- Sin `--name`: Docker genera nombre aleatorio

### 5. Ciclo de Vida Docker
```
docker build → docker run → docker start/stop → docker rm
     ↓              ↓               ↓                ↓
  Imagen      Contenedor       Gestión         Limpieza
```

---

## 🐛 TROUBLESHOOTING

### Problema 1: Puerto ya en uso
```bash
# Error: "port is already allocated"
# Solución:
docker stop $(docker ps -q)  # Detener todos los contenedores
docker ps  # Verificar que no hay ninguno corriendo
```

### Problema 2: Imagen no se descarga
```bash
# Verificar conectividad
ping hub.docker.com

# Reintentar pull
docker pull rodyuzuriaga/infinite-axis:latest
```

### Problema 3: Contenedor no inicia
```bash
# Ver logs detallados
docker logs infinite-axis

# Ejecutar en modo interactivo para debug
docker run -it --rm infinite-axis bash
```

### Problema 4: Sin espacio en disco
```bash
# Limpiar recursos
docker system prune -a --volumes
docker system df
```

---

## ✅ CHECKLIST FINAL

- [ ] ✅ Código subido a GitHub
- [ ] ✅ Secrets configurados (DOCKER_USERNAME, DOCKER_PASSWORD)
- [ ] ✅ GitHub Actions ejecutado exitosamente
- [ ] ✅ Imagen publicada en Docker Hub
- [ ] ✅ Probado en Play with Docker
- [ ] ✅ Aplicación accesible desde navegador
- [ ] ✅ Probado subir imagen y generar ángulos
- [ ] ✅ Comandos del taller ejecutados

---

## 📚 RECURSOS ADICIONALES

- **Repositorio GitHub**: https://github.com/rodyuzuriaga/Infinite-Axis
- **Docker Hub**: https://hub.docker.com/r/rodyuzuriaga/infinite-axis
- **Play with Docker**: https://labs.play-with-docker.com/
- **Docker Docs**: https://docs.docker.com/

---

## 🎉 ¡TALLER COMPLETADO!

Has aprendido:
1. ✅ Crear y gestionar contenedores Docker
2. ✅ Construir imágenes desde Dockerfile
3. ✅ Publicar imágenes en Docker Hub
4. ✅ Automatizar CI/CD con GitHub Actions
5. ✅ Desplegar aplicaciones en Play with Docker

**Próximos pasos:**
- Agregar tests automatizados
- Implementar multi-stage builds
- Usar Docker Secrets para credenciales
- Explorar Docker Swarm o Kubernetes
