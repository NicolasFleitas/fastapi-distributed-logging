# 🚀 FastAPI Logging Service

Sistema de logging distribuido construido con FastAPI y PostgreSQL. Permite que múltiples servicios envíen logs centralizados con autenticación mediante tokens.

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repo>
cd 05_logging_fast_api
```

### 2. Crear entorno virtual e instalar dependencias
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requeriments.txt
```

### 3. Configurar PostgreSQL
Asegúrate de tener PostgreSQL instalado y actualiza `database.py` con tus credenciales.

## 🏃 Cómo ejecutar la API

### Opción 1: Usar el script de PowerShell (Recomendado)
```powershell
.\run_api.ps1
```

### Opción 2: Usar el archivo batch
```cmd
run_api.bat
```

### Opción 3: Comando manual
```powershell
# Activar el entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Acceder a la documentación

Una vez que el servidor esté corriendo:

- **Swagger UI (Interactive docs)**: http://localhost:8000/docs
- **ReDoc (Alternative docs)**: http://localhost:8000/redoc
- **API Base URL**: http://localhost:8000

## 🔐 Autenticación con Tokens

Cada servicio tiene su propio token único. La API usa autenticación **Bearer Token**.

### Tokens de Servicio

| Servicio | Token | Descripción |
|----------|-------|-------------|
| **pagos** | `tok_pagos_prod_a1b2c3d4e5f6` | Procesa pagos y transacciones |
| **ventas** | `tok_ventas_prod_g7h8i9j0k1l2` | Gestiona el flujo de ventas |
| **auth** | `tok_auth_prod_m3n4o5p6q7r8` | Maneja autenticación y autorización |
| **notificaciones** | `tok_notif_prod_s9t0u1v2w3x4` | Envía emails, SMS y push notifications |
| **inventario** | `tok_invent_prod_y5z6a7b8c9d0` | Controla stock y almacenes |

### Cómo usar en /docs (Swagger UI)

1. Ve a http://localhost:8000/docs
2. Haz clic en el botón **🔓 Authorize** (arriba a la derecha)
3. Copia y pega uno de los tokens de la tabla
4. Haz clic en **Authorize**
5. ¡Listo! Ahora puedes probar los endpoints

## 📝 Ejemplos de uso

### Crear un log (POST)

```bash
curl -X POST "http://localhost:8000/logs" \
  -H "Authorization: Bearer tok_pagos_prod_a1b2c3d4e5f6" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "pagos",
    "severity": "INFO",
    "message": "Pago procesado correctamente",
    "timestamp": "2025-11-25T22:00:00"
  }'
```

### Obtener logs (GET)

**⚠️ IMPORTANTE:** La API ahora implementa **aislamiento de servicios**. Cada servicio solo puede ver sus propios logs basándose en el token que utiliza para autenticarse.

#### Obtener todos los logs del servicio autenticado
```bash
# Este request solo devolverá logs de 'pagos'
curl -X GET "http://localhost:8000/logs" \
  -H "Authorization: Bearer tok_pagos_prod_a1b2c3d4e5f6"
```

#### Intentar acceder a logs de otro servicio (❌ Rechazado)
```bash
# Esto devolverá un error 403 Forbidden
curl -X GET "http://localhost:8000/logs?service=ventas" \
  -H "Authorization: Bearer tok_pagos_prod_a1b2c3d4e5f6"

# Error: "No tienes permiso para ver logs de 'ventas'. 
#         Solo puedes ver logs de 'pagos'."
```

### Filtrar logs por rango de fechas

```bash
# Solo devolverá logs de 'pagos' dentro del rango de fechas
curl -X GET "http://localhost:8000/logs?timestamp_start=2025-11-25T00:00:00&timestamp_end=2025-11-26T00:00:00" \
  -H "Authorization: Bearer tok_pagos_prod_a1b2c3d4e5f6"
```

### Filtrar logs por severidad

```bash
# Solo devolverá logs de tipo ERROR del servicio autenticado
curl -X GET "http://localhost:8000/logs?severity=ERROR" \
  -H "Authorization: Bearer tok_auth_prod_m3n4o5p6q7r8"
```

## 🎯 Simulador de tráfico

El proyecto incluye un simulador que genera logs automáticamente de los 5 servicios:

```bash
python simulator.py
```

Esto generará logs continuos con mensajes realistas para cada servicio. Presiona `Ctrl+C` para detenerlo.

### Ejemplo de salida del simulador:
```
🚀 Iniciando simulación de tráfico distribuido...
📡 Simulando 5 servicios diferentes
================================================================================
✅ [PAGOS] INFO: Pago procesado exitosamente - Monto: $2500...
⚠️ [INVENTARIO] WARNING: Alerta: Stock crítico en producto ID 321...
❌ [AUTH] ERROR: Intento de login fallido - Contraseña incorrecta...
```

## 📁 Estructura del proyecto

```
05_logging_fast_api/
├── main.py              # Aplicación FastAPI principal con endpoints
├── models.py            # Modelos SQLAlchemy (tablas de base de datos)
├── schemas.py           # Esquemas Pydantic (validación de datos)
├── database.py          # Configuración de la base de datos PostgreSQL
├── simulator.py         # Simulador de logs para testing
├── run_api.ps1          # Script PowerShell para ejecutar la API
├── run_api.bat          # Script batch para ejecutar la API
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Esta documentación
```

## 🛠️ Tecnologías utilizadas

- **FastAPI** - Framework web moderno y de alto rendimiento
- **SQLAlchemy** - ORM (Object-Relational Mapping) para Python
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos y serialización
- **Uvicorn** - Servidor ASGI para aplicaciones Python async

## 📊 Endpoints disponibles

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/logs` | Crear un nuevo log | Bearer Token |
| GET | `/logs` | Obtener logs (con filtros opcionales) | Bearer Token |
| GET | `/docs` | Documentación interactiva Swagger | No requerida |
| GET | `/redoc` | Documentación alternativa ReDoc | No requerida |

### Parámetros de filtro para GET /logs

**🔒 Filtro Automático:** Todos los requests GET solo devuelven logs del servicio asociado al token utilizado.

#### Filtros adicionales disponibles:

- `service` - ⚠️ **Validado automáticamente**: Debe coincidir con el servicio del token o devolverá error 403
- `timestamp_start` - Fecha/hora de inicio del evento (ISO 8601)
- `timestamp_end` - Fecha/hora de fin del evento (ISO 8601)  
- `received_at_start` - Filtrar por cuándo se recibió el log (inicio)
- `received_at_end` - Filtrar por cuándo se recibió el log (fin)
- `severity` - Filtrar por nivel: `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## 🔒 Seguridad y Aislamiento de Servicios

### Autenticación
- Todos los endpoints (excepto `/docs` y `/redoc`) requieren autenticación con **Bearer Token**
- Los tokens son validados en cada request
- Cada servicio tiene su token único e irrepetible
- Token inválido → Error **401 Unauthorized**

### Aislamiento de Servicios (Service Isolation)
**📌 Característica de seguridad implementada:**

Cada servicio **solo puede acceder a sus propios logs**. La API automáticamente:

1. **Identifica el servicio** asociado al token en cada request
2. **Filtra automáticamente** los logs para mostrar solo los de ese servicio
3. **Bloquea intentos** de acceder a logs de otros servicios (Error 403 Forbidden)

#### Ejemplo de aislamiento:
```bash
# Servicio de Pagos hace un GET con su token
GET /logs + Token: tok_pagos_prod_a1b2c3d4e5f6
→ ✅ Devuelve SOLO logs de "pagos"

# Servicio de Ventas hace un GET con su token
GET /logs + Token: tok_ventas_prod_g7h8i9j0k1l2  
→ ✅ Devuelve SOLO logs de "ventas"

# Intento de acceso cruzado
GET /logs?service=ventas + Token: tok_pagos_prod_a1b2c3d4e5f6
→ ❌ Error 403: No tienes permiso para ver logs de otro servicio
```

### Mejores prácticas de seguridad
- 🔑 En producción, almacenar tokens en **variables de entorno** o **servicios de gestión de secretos** (AWS Secrets Manager, HashiCorp Vault)
- 🔄 Implementar **rotación de tokens** periódicamente
- 📝 Mantener **auditoría** de todos los accesos a logs
- 🚫 Nunca commitear tokens en el código fuente

## 🚧 Mejoras futuras

- [ ] Implementar rate limiting
- [ ] Agregar paginación a los endpoints GET
- [ ] Implementar búsqueda de texto completo en logs
- [ ] Agregar métricas y monitoreo con Prometheus
- [ ] Implementar rotación de logs antiguos
- [ ] Dashboard web para visualizar logs en tiempo real

## 📝 Notas

- El servidor auto-recarga cuando detecta cambios en el código (`--reload`)
- Los logs se almacenan en PostgreSQL con timestamp de recepción automático
- El simulador genera aproximadamente 2 logs por segundo

---

**Desarrollado con ❤️ usando FastAPI y PostgreSQL**
