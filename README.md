# EDAN Salud Mental - Ñuble

> Instrumento digital de Evaluación de Daños y Análisis de Necesidades en Salud Mental y Comunitaria.

**Colaboración:** Gobierno Regional de Ñuble / Servicio de Salud Ñuble  
**Contexto:** Incendios Forestales Región de Ñuble 2026

---

## 🚀 Quick Start

### Requisitos
- Docker y Docker Compose
- Python 3.12+ (para desarrollo local)

### Levantar con Docker
```bash
# Clonar y entrar al directorio
cd edan_sm_nuble

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f web
```

Acceder a: **http://localhost:5001**

### Desarrollo Local
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Ejecutar
flask run --port 5001
```

---

## 📁 Estructura del Proyecto

```
edan_sm_nuble/
├── app/
│   ├── __init__.py         # Factory de aplicación Flask
│   ├── constants/          # Constantes del instrumento EDAN
│   │   ├── factores.py     # Factores de riesgo y protectores
│   │   ├── recursos.py     # Recursos humanos, materiales, económicos
│   │   └── necesidades.py  # Necesidades psicosociales, institucionales, básicas
│   ├── data_maestros.py    # Datos maestros (comunas, establecimientos)
│   ├── models/             # Modelos SQLAlchemy
│   │   ├── enums.py        # Enumeraciones (SeccionEDAN, TipoRespuesta, etc.)
│   │   ├── edan.py         # Evaluador, FormularioEDAN
│   │   ├── catalogo.py     # CatalogoEDAN
│   │   └── respuesta.py    # RespuestaEDAN
│   ├── routes/             # Rutas Flask
│   │   └── formulario.py   # Wizard de 6 pasos
│   ├── services/           # Lógica de negocio
│   │   └── edan_service.py # EdanService
│   ├── static/             # Assets estáticos
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   └── templates/          # Templates Jinja2
│       ├── components/     # Componentes reutilizables
│       └── wizard/         # Pasos del formulario
├── docs/                   # Documentación
├── scripts/                # Scripts de utilidad
│   └── seed_catalogo.py    # Poblar catálogo EDAN
├── tests/                  # Tests pytest
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🧪 Tests

```bash
# Instalar pytest si no está instalado
pip install pytest

# Ejecutar todos los tests
pytest

# Con coverage
pip install pytest-cov
pytest --cov=app tests/
```

---

## 📊 Base de Datos

### Poblar Catálogo EDAN
```bash
# Desde la raíz del proyecto
python scripts/seed_catalogo.py

# Forzar reemplazo de ítems existentes
python scripts/seed_catalogo.py --force
```

### Migraciones
```bash
# Crear migración
flask db migrate -m "Descripción del cambio"

# Aplicar migración
flask db upgrade
```

---

## 🔧 Configuración

Variables de entorno (`.env`):

| Variable            | Descripción                      | Default    |
| ------------------- | -------------------------------- | ---------- |
| `FLASK_ENV`         | Entorno (development/production) | production |
| `SECRET_KEY`        | Clave secreta para sesiones      | -          |
| `DATABASE_URL`      | URI de PostgreSQL                | -          |
| `POSTGRES_USER`     | Usuario de BD                    | edan       |
| `POSTGRES_PASSWORD` | Contraseña de BD                 | -          |
| `POSTGRES_DB`       | Nombre de BD                     | edan_db    |

---

## 📝 Licencia

Proyecto desarrollado para uso del Gobierno Regional de Ñuble y Servicio de Salud Ñuble.

© 2026 GORE Ñuble

---

## 🚀 Guía de Despliegue en Servidor (Hetzner + Traefik)

Esta guía asume que el servidor ya cuenta con **Traefik** configurado y una red externa llamada `web`.

### Paso 1: Copiar Archivos al Servidor

Copiar la carpeta del proyecto vía `scp` o clonar el repositorio:

```bash
# Ejemplo con SCP
scp -r edan_sm_nuble usuario@servidor:/ruta/destino/
```

### Paso 2: Configurar Variables de Entorno

Crear archivo `.env` en el servidor con las credenciales de producción:

```bash
cp .env.example .env
nano .env
```

Asegurarse de definir `FLASK_ENV=production` y una `SECRET_KEY` segura.

### Paso 3: Desplegar Contenedores

```bash
# Construir y levantar servicios en segundo plano
docker-compose up -d --build
```

> **Nota:** El `docker-compose.yml` está configurado para conectarse el dominio `edan.138.201.53.205.nip.io` automáticamente vía Traefik.

### Paso 4: Poblar Catálogo

Una vez que los contenedores estén corriendo (healthy), ejecutar el script para cargar los ítems del instrumento:

```bash
# Ejecutar script dentro del contenedor
docker-compose exec web python scripts/seed_catalogo.py --force
```

### Paso 5: Verificación

- Revisar logs: `docker-compose logs -f web`
- Verificar healthcheck: `docker ps` (debe mostrar state `healthy`)
- Acceder al navegador: `https://edan.138.201.53.205.nip.io`
