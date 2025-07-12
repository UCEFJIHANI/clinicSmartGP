# Utilise une image officielle Python
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de l'app
COPY . .

# Installe les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Collecte les fichiers statiques
#RUN python manage.py collectstatic --noinput

# Applique les migrations et crée un superuser avec des variables d’env.
RUN python manage.py migrate && \
    python manage.py createsuperuser --noinput || true

# Expose le port (Railway utilisera automatiquement $PORT)
EXPOSE 8000

# Commande de lancement avec gunicorn
CMD ["gunicorn", "clinicSmart.wsgi", "--bind", "0.0.0.0:8000"]
