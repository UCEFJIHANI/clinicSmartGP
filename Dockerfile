# Utilise une image officielle Python avec plus de paquets préinstallés
FROM python:3.11-bullseye

# Étape 1: Installer les dépendances système minimales
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libpango-1.0-0 \
    libcairo2 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Étape 2: Configurer l'environnement
WORKDIR /app

# Étape 3: Télécharger directement les images nécessaires depuis CDN
RUN mkdir -p static/css/images/ && \
    cd static/css/images/ && \
    curl -O https://code.jquery.com/ui/1.13.2/themes/base/images/ui-icons_444444_256x240.png && \
    curl -O https://code.jquery.com/ui/1.13.2/themes/base/images/ui-icons_555555_256x240.png && \
    curl -O https://code.jquery.com/ui/1.13.2/themes/base/images/ui-bg_flat_75_ffffff_40x100.png

# Étape 4: Installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Étape 5: Copier l'application
COPY . .

# Configuration pour la production
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=clinicSmart.settings \
    PORT=8000

EXPOSE $PORT

# Ajoute ce fichier Python
COPY createsuper.py /app/createsuper.py
# Commande de lancement
CMD ["bash", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && python createsuper.py && gunicorn clinicSmart.wsgi --bind 0.0.0.0:$PORT"]




