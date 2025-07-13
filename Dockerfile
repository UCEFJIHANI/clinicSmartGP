# Utilise une image officielle Python
FROM python:3.11-slim

# Étape 1: Installer les dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
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

# Étape 2: Configurer l'environnement
WORKDIR /app

# Étape 3: Télécharger les assets nécessaires (version alternative avec curl)
RUN mkdir -p static/css/images/ && \
    curl -o /tmp/jquery-ui-icons.zip https://jqueryui.com/resources/download/jquery-ui-1.13.2.zip && \
    unzip /tmp/jquery-ui-icons.zip -d /tmp && \
    cp /tmp/jquery-ui-1.13.2/themes/base/images/* static/css/images/ && \
    rm -rf /tmp/jquery-ui*

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

# Commande de lancement
CMD ["bash", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn clinicSmart.wsgi --bind 0.0.0.0:$PORT"]
