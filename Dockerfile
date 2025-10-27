# Forex Trading Analysis App - Render.com
# Dockerfile per deployment su Render

FROM python:3.11-slim

# Imposta working directory
WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Installa dipendenze Python (senza TA-Lib che richiede compilazione)
RUN pip install --no-cache-dir -r requirements.txt || \
    (pip uninstall -y TA-Lib ta-lib && pip install --no-cache-dir -r requirements.txt)

# Copia tutto il codice
COPY . .

# Esponi porta (Render assegna PORT automaticamente)
EXPOSE 5000

# Avvia app
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
