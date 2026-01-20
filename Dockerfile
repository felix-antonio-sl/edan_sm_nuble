FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear usuario no privilegiado
RUN useradd -m -u 1000 edan

# Copiar código de la aplicación y ajustar permisos
COPY . .
RUN chown -R edan:edan /app

# Cambiar al usuario edan
USER edan

# Exponer puerto
EXPOSE 5000

# Comando para producción con Gunicorn
# Aumentamos timeout a 120s para evitar cortes prematuros
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()"]
