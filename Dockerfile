# Utilise une image officielle Python
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Installe les dépendances système
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    libjpeg-dev \
    libpng-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie les fichiers nécessaires
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie le reste de l'application
COPY . .

# Configuration pour la production
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=clinicSmart.settings \
    PORT=8000

# Expose le port (Railway utilisera automatiquement $PORT)
EXPOSE $PORT

# Commande de lancement (intègre le Procfile)
CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn clinicSmart.wsgi --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --access-logfile -"
