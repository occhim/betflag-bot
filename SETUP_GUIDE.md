# Guida Setup Completa - Forex Trading Analysis App

Guida passo-passo per avviare l'applicazione da zero.

---

## Indice

1. [Prerequisiti](#prerequisiti)
2. [Installazione Python](#installazione-python)
3. [Installazione TA-Lib](#installazione-ta-lib)
4. [Registrazione OANDA](#registrazione-oanda)
5. [Setup Progetto](#setup-progetto)
6. [Primo Avvio](#primo-avvio)
7. [Verifica Funzionamento](#verifica-funzionamento)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisiti

Prima di iniziare, assicurati di avere:
- Computer con Windows, macOS o Linux
- Connessione internet
- 15-30 minuti di tempo
- (Opzionale) Editor di testo (VS Code, Sublime, etc.)

---

## 1. Installazione Python

### Windows

**1.1 Scarica Python**
- Vai su https://www.python.org/downloads/
- Clicca su "Download Python 3.11.x" (versione più recente)
- Salva il file `python-3.11.x-amd64.exe`

**1.2 Installa Python**
```
1. Doppio click sul file scaricato
2. ✅ IMPORTANTE: Spunta "Add Python to PATH"
3. Clicca "Install Now"
4. Attendi completamento
5. Clicca "Close"
```

**1.3 Verifica Installazione**
```bash
# Apri Prompt dei Comandi (Win + R, digita "cmd")
python --version
# Dovresti vedere: Python 3.11.x

pip --version
# Dovresti vedere: pip 23.x.x
```

### macOS

**1.1 Installa Homebrew** (se non lo hai già)
```bash
# Apri Terminale (Cmd + Spazio, digita "Terminal")
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**1.2 Installa Python**
```bash
brew install python@3.11
```

**1.3 Verifica**
```bash
python3 --version
pip3 --version
```

### Linux (Ubuntu/Debian)

```bash
# Apri Terminale
sudo apt update
sudo apt install python3.11 python3-pip python3-venv

# Verifica
python3 --version
pip3 --version
```

---

## 2. Installazione TA-Lib

TA-Lib è una libreria C per analisi tecnica. È la parte più complessa dell'installazione.

### Windows

**Opzione A: Installer Pre-compilato (CONSIGLIATO)**

```bash
# 1. Scarica il file .whl appropriato da:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

# Per Python 3.11 64-bit, scarica:
# TA_Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl

# 2. Apri Prompt dei Comandi nella cartella Download
cd C:\Users\TUO_NOME\Downloads

# 3. Installa il file .whl
pip install TA_Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl
```

**Opzione B: Compilazione da Sorgente**

Se l'opzione A non funziona:

```bash
# 1. Installa Visual Studio Build Tools
# Scarica da: https://visualstudio.microsoft.com/downloads/
# Seleziona "Desktop development with C++"

# 2. Scarica TA-Lib C library
# Da: http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-msvc.zip

# 3. Estrai in C:\ta-lib

# 4. Installa
pip install ta-lib
```

### macOS

```bash
# Installa TA-Lib via Homebrew
brew install ta-lib

# Poi installa il wrapper Python
pip3 install ta-lib
```

### Linux (Ubuntu/Debian)

```bash
# Installa dipendenze di build
sudo apt-get update
sudo apt-get install -y build-essential wget

# Scarica e compila TA-Lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Installa wrapper Python
pip3 install ta-lib
```

**Verifica Installazione TA-Lib**
```bash
python -c "import talib; print('TA-Lib OK')"
# Dovresti vedere: TA-Lib OK
```

---

## 3. Registrazione OANDA

OANDA fornisce API gratuite per dati forex in tempo reale.

### 3.1 Crea Account Demo (GRATUITO)

```
1. Vai su: https://www.oanda.com/
2. Clicca "Try Free Demo"
3. Compila il form:
   - Nome, Email, Password
   - Paese
   - Esperienza trading (puoi mettere "Beginner")
4. Clicca "Open Account"
5. Verifica email (controlla inbox/spam)
6. Login su: https://www.oanda.com/
```

### 3.2 Ottieni API Token

```
1. Login su OANDA
2. Vai su "Manage Funds" → "Manage API Access"
   Oppure: https://www.oanda.com/account/tpa/personal_token
3. Clicca "Generate" per creare un token
4. COPIA e SALVA il token (appare solo una volta!)
   Esempio: 1a2b3c4d5e6f7g8h9i0j-abcdefghijklmnop
5. Copia anche il tuo Account ID (numero sotto il tuo nome)
   Esempio: 101-001-1234567-001
```

**⚠️ IMPORTANTE**: Non condividere mai il tuo API token!

---

## 4. Setup Progetto

### 4.1 Scarica il Progetto

**Opzione A: Con Git**
```bash
# Se hai Git installato
git clone https://github.com/occhim/betflag-bot.git
cd betflag-bot
```

**Opzione B: Download Manuale**
```
1. Vai su: https://github.com/occhim/betflag-bot
2. Clicca "Code" → "Download ZIP"
3. Estrai la cartella ZIP
4. Apri Terminale/Prompt nella cartella estratta
```

### 4.2 Crea Virtual Environment (CONSIGLIATO)

Isola le dipendenze del progetto dal sistema.

**Windows:**
```bash
# Nella cartella del progetto
python -m venv venv

# Attiva virtual environment
venv\Scripts\activate

# Dovresti vedere (venv) prima del prompt
```

**macOS/Linux:**
```bash
# Nella cartella del progetto
python3 -m venv venv

# Attiva virtual environment
source venv/bin/activate

# Dovresti vedere (venv) prima del prompt
```

### 4.3 Installa Dipendenze Python

```bash
# Con virtual environment attivato
pip install -r requirements.txt

# Attendi 2-5 minuti per il download
# Dovresti vedere "Successfully installed..."
```

**Verifica Installazione:**
```bash
pip list
# Dovresti vedere: pandas, flask, oandapyV20, etc.
```

### 4.4 Configura API OANDA

**Crea file .env:**

**Windows:**
```bash
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
# Oppure usa il tuo editor preferito
```

**Modifica il file .env:**
```bash
# Sostituisci con i TUOI dati OANDA
OANDA_API_KEY=1a2b3c4d5e6f7g8h9i0j-abcdefghijklmnop
OANDA_ACCOUNT_ID=101-001-1234567-001
OANDA_ENVIRONMENT=practice

# Configurazione App
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

**Salva e chiudi** (Ctrl+S, Ctrl+X in nano)

---

## 5. Primo Avvio

### 5.1 Test Connessione OANDA

Prima testiamo se le API funzionano:

```bash
python -c "from src.oanda_client import OandaClient; client = OandaClient(); print('Connection OK' if client.get_current_price('EUR_USD') else 'Connection FAILED')"
```

**Risultato Atteso:** `Connection OK`

Se vedi errori, controlla:
- API key corretta in .env
- Account ID corretto
- Connessione internet attiva

### 5.2 Esegui Esempi

```bash
python example.py
```

**Cosa aspettarsi:**
```
============================================================
FOREX TRADING ANALYSIS APP - EXAMPLES
============================================================

EXAMPLE 1: Multi-Pair Scanner
============================================================

1. Scanning EUR/USD on H4 timeframe...

Pair: EUR_USD
Current Price: 1.08543
At Key Level: True

Recent Patterns:
  - 2025-01-15 16:00:00: bullish_hammer

Trading Signals:
  - BUY: bullish_hammer at support level
    Entry: 1.08543
    Stop: 1.08323
    Target: 1.08983
    R/R: 1:2.0
```

**Se richiesto**, rispondi:
```
Run backtesting example? (takes ~30 seconds) [y/N]: y
```

### 5.3 Avvia Web App

```bash
python app.py
```

**Output Atteso:**
```
╔════════════════════════════════════════════════════╗
║   Forex Trading Analysis App                       ║
║   Price Action & Pattern Recognition System        ║
╚════════════════════════════════════════════════════╝

Server running on: http://localhost:5000

API Endpoints:
- GET  /api/health              - Health check
- GET  /api/pairs               - Available pairs
- GET  /api/scan/<pair>         - Scan single pair
...

 * Running on http://0.0.0.0:5000
 * Restarting with stat
```

**Apri Browser:**
```
http://localhost:5000
```

Dovresti vedere la dashboard con:
- Controlli (timeframe selector, bottoni)
- Statistiche (segnali attivi, buy/sell)
- Cards con segnali forex

---

## 6. Verifica Funzionamento

### 6.1 Test Dashboard Web

1. **Apri** http://localhost:5000
2. **Clicca** "Scan All Pairs"
3. **Attendi** 10-30 secondi
4. **Verifica**:
   - Statistiche aggiornate
   - Cards con segnali BUY/SELL/WATCH
   - Pattern rilevati

### 6.2 Test API Endpoints

**Apri un nuovo terminale** (lascia l'app in esecuzione)

```bash
# Test health check
curl http://localhost:5000/api/health

# Dovresti vedere:
# {"status":"healthy","version":"1.0.0","api_configured":true}

# Test scan singola coppia
curl http://localhost:5000/api/scan/EUR_USD?timeframe=H4

# Dovresti vedere JSON con patterns, livelli S/R, segnali
```

### 6.3 Test Programmatico

Crea file `test.py`:

```python
from src.scanner import ForexScanner

scanner = ForexScanner()
signals = scanner.get_active_signals(timeframe='H4')

print(f"Segnali attivi: {len(signals)}")
for signal in signals[:3]:
    print(f"{signal['pair']}: {signal['type']} - R/R 1:{signal.get('risk_reward', 'N/A')}")
```

Esegui:
```bash
python test.py
```

---

## 7. Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'talib'"

**Soluzione:**
```bash
# TA-Lib non installato correttamente
# Rivedi sezione "Installazione TA-Lib"

# Quick fix (usa libreria alternativa):
pip uninstall ta-lib
# Modifica requirements.txt: sostituisci ta-lib==0.4.28 con ta==0.11.0
pip install ta==0.11.0
```

### Problema: "oandapyV20.exceptions.V20Error: Unauthorized"

**Soluzione:**
```bash
# API key errata in .env
# Verifica:
cat .env  # Linux/Mac
type .env # Windows

# Controlla:
# 1. API key copiata correttamente (nessuno spazio extra)
# 2. Account ID corretto
# 3. OANDA_ENVIRONMENT=practice
```

### Problema: "Address already in use" (porta 5000)

**Soluzione:**
```bash
# Opzione 1: Cambia porta in .env
PORT=8000

# Opzione 2: Killa processo sulla porta 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

### Problema: "No data available" / API non risponde

**Soluzione:**
```bash
# 1. Verifica connessione internet
ping www.google.com

# 2. Verifica OANDA practice environment attivo
# Login su OANDA e controlla account demo

# 3. Limiti rate API
# OANDA practice: max 120 req/ora
# Attendi 5 minuti e riprova
```

### Problema: Python non trovato (Windows)

**Soluzione:**
```bash
# Python non in PATH
# 1. Disinstalla Python
# 2. Reinstalla e ✅ SPUNTA "Add to PATH"
# 3. Riavvia Prompt dei Comandi
```

### Problema: pip install fallisce con errori di compilazione

**Soluzione:**
```bash
# Aggiorna pip
python -m pip install --upgrade pip setuptools wheel

# Riprova
pip install -r requirements.txt
```

---

## 8. Utilizzo Quotidiano

### Avvio Rapido

```bash
# 1. Apri terminale nella cartella progetto
cd /percorso/to/betflag-bot

# 2. Attiva virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Avvia app
python app.py

# 4. Apri browser
http://localhost:5000
```

### Aggiornare Dati

L'app scarica dati in tempo reale ad ogni scan. Non serve aggiornare manualmente.

### Chiudere l'App

```bash
# Nel terminale dove gira l'app
Ctrl + C

# Disattiva virtual environment
deactivate
```

---

## 9. Prossimi Passi

Ora che l'app funziona:

1. **Studia i Pattern**
   - Leggi README_FOREX.md
   - Esegui backtesting: `python example.py`
   - Analizza win rate dei vari pattern

2. **Testa su Demo**
   - Usa solo account OANDA practice
   - Segna i segnali su un foglio
   - Verifica se avrebbero dato profitto

3. **Personalizza**
   - Modifica `config.py` per cambiare:
     - Coppie forex da scansionare
     - Timeframe
     - Risk/Reward minimo
     - Tolleranza livelli S/R

4. **Automatizza**
   - Crea script per scansioni periodiche
   - Integra alert via email/Telegram
   - Esporta segnali in CSV

---

## 10. Supporto

### Documentazione
- **README.md** - Overview
- **README_FOREX.md** - Documentazione completa
- **SETUP_GUIDE.md** - Questa guida

### Risorse
- [OANDA API Docs](https://developer.oanda.com/rest-live-v20/introduction/)
- [TA-Lib Install Guide](https://github.com/TA-Lib/ta-lib-python)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Help
- Apri issue su GitHub
- Controlla sezione Troubleshooting sopra

---

## Checklist Setup Completo

- [ ] Python 3.8+ installato
- [ ] pip funzionante
- [ ] TA-Lib installato
- [ ] Account OANDA demo creato
- [ ] API Token OANDA ottenuto
- [ ] Progetto scaricato
- [ ] Virtual environment creato
- [ ] Dipendenze installate (pip install -r requirements.txt)
- [ ] File .env configurato
- [ ] Test connessione OK
- [ ] example.py eseguito senza errori
- [ ] Web app avviata (python app.py)
- [ ] Dashboard aperta su http://localhost:5000
- [ ] Segnali visualizzati correttamente

**Se tutti i punti sono ✅ sei pronto per usare l'app!**

---

**Buon Trading!** 📈

*Ricorda: Testa sempre su account demo prima di usare denaro reale.*
