# Utilise une image officielle Python avec les dépendances graphiques préinstallées
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Installe les dépendances système COMPLÈTES pour WeasyPrint
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
    pango1.0-tools \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie le code de l'application
COPY . .

# Configuration pour la production
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=clinicSmart.settings \
    PORT=8000

# Exposition du port
EXPOSE $PORT

# Commande de lancement optimisée
CMD bash -c "python manage.py check --deploy && \
             python manage.py migrate && \
             python manage.py collectstatic --noinput && \
             gunicorn clinicSmart.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120"
