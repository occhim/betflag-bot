# Quick Start - Forex Trading Analysis App

Guida veloce per partire in 5 minuti (se hai già Python e TA-Lib).

---

## Setup Automatico

### Linux/macOS

```bash
# 1. Esegui script di setup
chmod +x setup.sh
./setup.sh

# 2. Configura OANDA
nano .env
# Modifica OANDA_API_KEY e OANDA_ACCOUNT_ID

# 3. Testa
python example.py

# 4. Avvia app
python app.py
```

### Windows

```cmd
REM 1. Esegui script di setup
setup.bat

REM 2. Configura OANDA
notepad .env
REM Modifica OANDA_API_KEY e OANDA_ACCOUNT_ID

REM 3. Testa
python example.py

REM 4. Avvia app
python app.py
```

---

## Setup Manuale Rapido

```bash
# 1. Installa dipendenze
pip install -r requirements.txt

# 2. Configura OANDA
cp .env.example .env
# Modifica .env con le tue credenziali

# 3. Test
python example.py

# 4. Avvia
python app.py
# Apri http://localhost:5000
```

---

## Uso Quotidiano

```bash
# Avvia app
python app.py

# Apri browser
http://localhost:5000

# Clicca "Scan All Pairs"
# Visualizza segnali BUY/SELL
```

---

## API Usage

```python
from src.scanner import ForexScanner

scanner = ForexScanner()

# Ottieni segnali
signals = scanner.get_active_signals(timeframe='H4')

for signal in signals:
    print(f"{signal['pair']}: {signal['type']}")
    print(f"  Entry: {signal['entry']}")
    print(f"  R/R: 1:{signal['risk_reward']}")
```

---

## Problemi?

Vedi **SETUP_GUIDE.md** per:
- Installazione TA-Lib
- Configurazione OANDA
- Troubleshooting completo

---

## Primi 3 Test

### 1. Test Connessione
```bash
python -c "from src.oanda_client import OandaClient; print('OK' if OandaClient().get_current_price('EUR_USD') else 'FAIL')"
```

### 2. Test Pattern Detection
```bash
python example.py
```

### 3. Test Web App
```bash
python app.py
# Apri http://localhost:5000
```

---

**Se tutti i test passano, sei pronto! 🚀**

Per guida completa: **SETUP_GUIDE.md**
