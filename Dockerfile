# Forex Trading Analysis App - Render.com
# Dockerfile per deployment su Render

FROM python:3.11-slim

# Imposta working directory
WORKDIR /app

# Installa dipendenze di sistema per TA-Lib
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Installa TA-Lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Copia requirements
COPY requirements.txt .

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice
COPY . .

# Esponi porta (Render assegna PORT automaticamente)
EXPOSE 5000

# Avvia app
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
