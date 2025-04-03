# Base image Python slim
FROM python:3.11-slim

#  Définir le dossier de travail dans le conteneur
WORKDIR /app

#  Copier tous les fichiers du service dans /app
COPY . /app

#  Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#  Exposer le port 8000 (facultatif mais clair)
EXPOSE 8000

# Démarrer le service FastAPI avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
