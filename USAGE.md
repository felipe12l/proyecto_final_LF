# 🔐 JWT Analyzer - Guía de Uso

Aplicación completa para analizar y generar JSON Web Tokens con análisis léxico, sintáctico y semántico.

## 📋 Requisitos

- Docker y Docker Compose
- Puertos disponibles: 3000 (frontend), 8000 (backend), 27017 (MongoDB)

## 🚀 Inicio Rápido

### 1. Configurar variables de entorno

Copia el archivo de ejemplo y ajusta si es necesario:

```bash
cp .env.example .env
```

### 2. Levantar los servicios

```bash
docker-compose up -d
```

Esto iniciará:
- **Frontend** (Vue 3 + Vite): http://localhost:3000
- **Backend** (FastAPI): http://localhost:8000
- **MongoDB**: localhost:27017

### 3. Acceder a la aplicación

Abre tu navegador en: **http://localhost:3000**

## 🎯 Funcionalidades

### Analizar Token JWT
1. Ve a la pestaña "Analizar JWT"
2. Pega tu token JWT o usa el botón "Cargar Ejemplo"
3. Haz clic en "Analizar Token"
4. Visualiza:
   - Header decodificado
   - Payload decodificado
   - Signature
   - Tokens léxicos (encoded, header, payload)
   - Errores de análisis si los hay

### Generar Token JWT
1. Ve a la pestaña "Generar JWT"
2. Configura el header (algoritmo)
3. Edita el payload (añade/elimina campos)
4. Ingresa tu secreto
5. Haz clic en "Generar Token"
6. Copia el token generado

## 📡 API Endpoints

### POST `/api/analyze`
Analiza un token JWT completo.

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (éxito):**
```json
{
  "status": "ok",
  "header": {"alg": "HS256", "typ": "JWT"},
  "payload": {"sub": "1234567890", "name": "John Doe"},
  "signature": "...",
  "tokens": {
    "encoded": [...],
    "header": [...],
    "payload": [...]
  }
}
```

**Response (error):**
```json
{
  "status": "error",
  "phase": "sintactico",
  "message": "Error en el análisis sintáctico"
}
```

### POST `/api/encode`
Genera un nuevo token JWT.

**Request:**
```json
{
  "header": {"alg": "HS256", "typ": "JWT"},
  "payload": {"sub": "user123", "name": "John"},
  "secret": "your-secret-key"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "header": {...},
  "payload": {...},
  "signature": "..."
}
```

## 🗄️ Base de Datos

La aplicación guarda automáticamente todos los análisis en MongoDB:

### Conectar a MongoDB

```bash
docker exec -it jwt-mongo mongosh
```

### Consultar análisis guardados

```javascript
use jwt_analyzer
db.analyses.find().pretty()
```

### Estructura del documento

```javascript
{
  "_id": ObjectId("..."),
  "token": "eyJhbGci...",
  "result": {
    "status": "ok",
    "header": {...},
    "payload": {...}
  },
  "created_at": ISODate("2025-11-22T...")
}
```

## 🛠️ Desarrollo

### Ver logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Reconstruir después de cambios

```bash
docker-compose up -d --build
```

### Ejecutar comandos en contenedores

```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh
```

### Instalar nuevas dependencias

**Backend:**
```bash
# Añadir en requirements.txt y luego:
docker-compose restart backend
```

**Frontend:**
```bash
docker-compose exec frontend npm install <paquete>
```

## 🔧 Configuración

### Variables de entorno (.env)

```bash
# URI de conexión a MongoDB (desde contenedor backend)
MONGO_URI=mongodb://db:27017

# Nombre de la base de datos
MONGO_DB=jwt_analyzer

# Timeout de conexión en milisegundos
MONGO_TIMEOUT_MS=2000
```

### Cambiar puertos

Edita `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Cambiar 3000 por el puerto deseado
  
  backend:
    ports:
      - "8001:8000"  # Cambiar 8000 por el puerto deseado
```

## 🐛 Troubleshooting

### El frontend no se conecta al backend

1. Verifica que los servicios estén corriendo:
   ```bash
   docker-compose ps
   ```

2. Revisa los logs del backend:
   ```bash
   docker-compose logs backend
   ```

3. Verifica la configuración de proxy en `frontend/vite.config.js`

### Error de conexión a MongoDB

1. Verifica que el contenedor de MongoDB esté corriendo:
   ```bash
   docker ps | grep mongo
   ```

2. Prueba la conexión:
   ```bash
   docker-compose exec backend python -c "from database.db import get_client; get_client().admin.command('ping'); print('OK')"
   ```

### Puerto ya en uso

```bash
# Detener servicios
docker-compose down

# Buscar proceso usando el puerto
lsof -i :3000
lsof -i :8000

# Cambiar puerto en docker-compose.yml
```

## 📦 Estructura del Proyecto

```
.
├── backend/
│   ├── controllers/      # Lógica de negocio
│   ├── database/         # Conexión MongoDB
│   ├── lexer/           # Análisis léxico
│   ├── semantic/        # Análisis semántico
│   ├── sintactic/       # Análisis sintáctico
│   ├── utils/           # Utilidades (decode, encode, etc.)
│   ├── main.py          # App FastAPI
│   └── routes.py        # Rutas API
├── frontend/
│   └── src/
│       ├── components/  # Componentes Vue
│       ├── App.vue      # Componente principal
│       └── main.js      # Entry point
├── database/
│   └── db.py           # Módulo de conexión (legacy)
└── docker-compose.yml  # Orquestación de servicios
```

## 🚀 Producción

Para desplegar en producción:

1. **Cambiar CORS en backend** (`backend/main.py`):
   ```python
   allow_origins=["https://tu-dominio.com"]
   ```

2. **Usar variables de entorno seguras**:
   - MongoDB con autenticación
   - Secretos seguros para JWT

3. **Construir frontend optimizado**:
   ```bash
   cd frontend
   npm run build
   ```

4. **Usar servidor web (nginx) para servir el frontend**

## 📝 Notas

- Los análisis se guardan automáticamente en MongoDB
- El frontend hace proxy de `/api/*` al backend en desarrollo
- Los tokens de ejemplo son válidos pero usan secretos de prueba
- Para producción, configura HTTPS y autenticación

## 🤝 Contribuir

Para añadir nuevas funcionalidades:

1. Backend: añade rutas en `routes.py` y controladores en `controllers/`
2. Frontend: crea componentes en `src/components/`
3. Reconstruye los contenedores: `docker-compose up -d --build`

## 📄 Licencia

Este proyecto es parte de un proyecto final de Lenguajes Formales.
