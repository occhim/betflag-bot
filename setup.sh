#!/bin/bash

# Forex Trading Analysis App - Setup Automatico (Linux/macOS)
# Script per installazione e configurazione automatica

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════╗"
echo "║   Forex Trading Analysis App - Setup              ║"
echo "║   Installazione Automatica                         ║"
echo "╚════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Funzione per stampare step
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# 1. Verifica Python
print_step "Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION trovato"
    PYTHON_CMD=python3
    PIP_CMD=pip3
else
    print_error "Python 3 non trovato. Installa Python 3.8+ da python.org"
    exit 1
fi

# 2. Verifica pip
print_step "Verificando pip..."
if command -v $PIP_CMD &> /dev/null; then
    PIP_VERSION=$($PIP_CMD --version 2>&1 | awk '{print $2}')
    print_success "pip $PIP_VERSION trovato"
else
    print_error "pip non trovato. Installa pip: sudo apt install python3-pip"
    exit 1
fi

# 3. Installa TA-Lib (parte più complessa)
print_step "Verificando TA-Lib..."
if $PYTHON_CMD -c "import talib" 2>/dev/null; then
    print_success "TA-Lib già installato"
else
    print_warning "TA-Lib non trovato. Installazione in corso..."

    # Rileva OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_step "Rilevato Linux. Installando TA-Lib..."

        # Installa dipendenze
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y build-essential wget
        fi

        # Scarica e compila TA-Lib
        wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
        tar -xzf ta-lib-0.4.0-src.tar.gz
        cd ta-lib/
        ./configure --prefix=/usr
        make
        sudo make install
        cd ..
        rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

        print_success "TA-Lib C library installata"

    elif [[ "$OSTYPE" == "darwin"* ]]; then
        print_step "Rilevato macOS. Installando TA-Lib via Homebrew..."

        # Verifica Homebrew
        if ! command -v brew &> /dev/null; then
            print_error "Homebrew non trovato. Installa da: https://brew.sh"
            exit 1
        fi

        brew install ta-lib
        print_success "TA-Lib installato via Homebrew"
    else
        print_error "OS non supportato per installazione automatica TA-Lib"
        print_warning "Installazione manuale richiesta. Vedi SETUP_GUIDE.md"
        exit 1
    fi
fi

# 4. Crea virtual environment
print_step "Creando virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment già esistente. Skip."
else
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment creato"
fi

# 5. Attiva virtual environment
print_step "Attivando virtual environment..."
source venv/bin/activate

# 6. Aggiorna pip
print_step "Aggiornando pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
print_success "pip aggiornato"

# 7. Installa dipendenze Python
print_step "Installando dipendenze Python (può richiedere 2-5 minuti)..."
pip install -r requirements.txt
print_success "Dipendenze installate"

# 8. Installa TA-Lib Python wrapper
print_step "Installando TA-Lib Python wrapper..."
pip install ta-lib || pip install ta  # Fallback a libreria alternativa
print_success "TA-Lib Python wrapper installato"

# 9. Configura .env
print_step "Configurando file .env..."
if [ -f ".env" ]; then
    print_warning "File .env già esistente. Skip."
else
    cp .env.example .env
    print_success "File .env creato da .env.example"
    print_warning "IMPORTANTE: Modifica .env con le tue credenziali OANDA!"
    echo ""
    echo -e "${YELLOW}Prossimi passi:${NC}"
    echo "1. Registrati su OANDA: https://www.oanda.com/"
    echo "2. Ottieni API Token e Account ID"
    echo "3. Modifica .env con: nano .env"
fi

# 10. Test installazione
print_step "Testando installazione..."

# Test import moduli
$PYTHON_CMD -c "import pandas; import flask; import oandapyV20; print('Imports OK')" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Test import moduli: OK"
else
    print_error "Test import moduli: FAILED"
    exit 1
fi

# Test TA-Lib
$PYTHON_CMD -c "import talib; print('TA-Lib OK')" > /dev/null 2>&1 || \
$PYTHON_CMD -c "import ta; print('TA OK')" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Test TA-Lib: OK"
else
    print_error "Test TA-Lib: FAILED"
    print_warning "Installazione manuale TA-Lib richiesta. Vedi SETUP_GUIDE.md"
fi

# 11. Riepilogo
echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════╗"
echo "║   Setup Completato!                                ║"
echo "╚════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${BLUE}Prossimi Passi:${NC}"
echo ""
echo "1. Configura OANDA API:"
echo -e "   ${YELLOW}nano .env${NC}"
echo "   Modifica OANDA_API_KEY e OANDA_ACCOUNT_ID"
echo ""
echo "2. Esegui esempi:"
echo -e "   ${YELLOW}python example.py${NC}"
echo ""
echo "3. Avvia web app:"
echo -e "   ${YELLOW}python app.py${NC}"
echo "   Poi apri: http://localhost:5000"
echo ""
echo "4. Leggi documentazione:"
echo -e "   ${YELLOW}cat SETUP_GUIDE.md${NC}"
echo ""

print_warning "Ricorda di attivare il virtual environment ad ogni sessione:"
echo -e "   ${YELLOW}source venv/bin/activate${NC}"

echo ""
echo -e "${GREEN}Buon Trading! 📈${NC}"
