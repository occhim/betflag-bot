# Pull Request - Forex Trading Analysis App

## 📊 Titolo
**Forex Trading Analysis App - Price Action & Pattern Recognition**

## 📝 Descrizione

### Implementazione Completa

App professionale di analisi tecnica per il trading forex basata su **Price Action** e riconoscimento automatico di pattern candlestick.

---

### ✨ Caratteristiche Implementate

#### 🕯️ Pattern Candlestick
- Pin Bar (Hammer / Shooting Star)
- Engulfing (Bullish / Bearish)
- Inside Bar (consolidamento)
- Doji (indecisione)
- Morning/Evening Star (inversioni)

#### 📈 Analisi Supporti e Resistenze
- Rilevamento automatico livelli chiave
- Clustering intelligente di pivot points
- Calcolo forza livelli (numero di tocchi)
- Identificazione livelli più vicini al prezzo

#### 🔍 Scanner Multi-Coppia
- Scansione simultanea di 7 coppie forex major
- Analisi multi-timeframe (H1, H4, Daily)
- Generazione automatica segnali BUY/SELL
- Filtro per pattern su livelli chiave

#### 💰 Risk Management
- Calcolo automatico Risk/Reward ratio
- Position sizing basato su % di rischio
- Stop Loss e Take Profit automatici
- Validazione R/R minimo (1.5:1)

#### 📉 Backtesting Engine
- Test storici su dati OANDA
- Statistiche: Win Rate, Profit Factor, Drawdown
- Simulazione trade completa

#### 🌐 Web Dashboard
- Interfaccia moderna responsive
- Segnali real-time
- REST API completa

---

### 🏗️ File Creati

**Core Application:**
- `src/oanda_client.py` - OANDA API integration
- `src/pattern_detector.py` - Pattern recognition
- `src/support_resistance.py` - S/R analysis
- `src/scanner.py` - Multi-pair scanner
- `src/backtester.py` - Backtesting engine
- `app.py` - Flask web app
- `templates/index.html` - Dashboard UI
- `config.py` - Configuration

**Documentation:**
- `README_FOREX.md` - Complete documentation
- `SETUP_GUIDE.md` - Step-by-step setup
- `QUICK_START.md` - Quick start guide
- `example.py` - Usage examples

**Setup Tools:**
- `setup.sh` - Auto setup (Linux/macOS)
- `setup.bat` - Auto setup (Windows)
- `requirements.txt` - Python dependencies
- `.env.example` - Config template
- `.gitignore` - Git ignore rules

**Updated:**
- `README.md` - Project overview

---

### 🚀 Come Testare

```bash
# 1. Setup
./setup.sh  # o setup.bat su Windows

# 2. Configura OANDA
cp .env.example .env
# Modifica .env con API credentials

# 3. Test
python example.py

# 4. Avvia
python app.py
# Apri http://localhost:5000
```

---

### 🎯 Strategia

**Price Action + Pattern Recognition**

1. Rileva pattern candlestick su livelli S/R
2. Verifica R/R minimo 1.5:1
3. Genera segnali BUY/SELL automatici

**Logica:**
- BUY: Pattern bullish su supporto
- SELL: Pattern bearish su resistenza

---

### 📦 Dipendenze

- Python 3.8+
- pandas, numpy, scipy
- TA-Lib (o libreria ta)
- oandapyV20
- Flask

---

### ⚠️ Disclaimer

Software educativo. Trading forex comporta rischi.
Testare sempre su account demo OANDA.

---

### 📊 Commits

- Add complete Forex Trading Analysis App with Price Action strategy
- Add comprehensive setup guides and automation scripts

---

**Pronto per il merge!** ✅

Tutta la documentazione e gli script di setup sono inclusi.
