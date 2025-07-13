# Utilise une image officielle Python avec les outils réseau
FROM python:3.11-slim

# Étape 1: Installer les dépendances système (y compris wget)
RUN apt-get update && apt-get install -y \
    wget \
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

# Étape 2: Installer les dépendances Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Étape 3: Télécharger les assets manquants avant la copie du code
RUN mkdir -p /app/static/css/images/ && \
    wget https://code.jquery.com/ui/1.12.1/themes/base/images/ui-icons_444444_256x240.png -O /app/static/css/images/ui-icons_444444_256x240.png

# Étape 4: Copier le code applicatif
COPY . .

# Configuration pour la production
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=clinicSmart.settings \
    PORT=8000

EXPOSE $PORT

# Commande de lancement
CMD bash -c "python manage.py collectstatic --noinput && \
             python manage.py migrate && \
             gunicorn clinicSmart.wsgi --bind 0.0.0.0:$PORT --workers 3 --timeout 120"
