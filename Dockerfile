# Utilise une image officielle Python
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de l'app
COPY . .
# Installe les bibliothèques système nécessaires à WeasyPrint
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
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# Installe les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Collecte les fichiers statiques
# RUN python manage.py collectstatic --noinput

# Applique les migrations et crée un superuser avec des variables d’env.
#RUN python manage.py migrate && \
 #   python manage.py createsuperuser --noinput || true

# Expose le port (Railway utilisera automatiquement $PORT)
EXPOSE 8000

# Commande de lancement avec gunicorn
#CMD ["gunicorn", "clinicSmart.wsgi", "--bind", "0.0.0.0:8000"]
