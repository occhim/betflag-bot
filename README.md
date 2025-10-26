# Forex Trading Analysis App

**App di analisi tecnica per il trading forex basata su Price Action e Pattern Recognition**

## Progetti nel Repository

Questo repository contiene:

1. **Forex Trading Analysis App** (PRINCIPALE) - Sistema completo di analisi tecnica forex
2. ~~BetFlag Bot~~ (Progetto precedente - deprecato)

---

## Forex Trading Analysis App

Sistema professionale per l'analisi tecnica nel trading forex, con riconoscimento automatico di pattern candlestick, supporti/resistenze, generazione segnali e backtesting.

### Caratteristiche

- **Pattern Candlestick**: Pin Bar, Engulfing, Inside Bar, Doji, Morning/Evening Star
- **Support/Resistance**: Rilevamento automatico livelli chiave
- **Scanner Multi-Coppia**: Analisi simultanea di 7 coppie major
- **Multi-Timeframe**: H1, H4, Daily
- **Risk Management**: Calcolo automatico R/R e position sizing
- **Backtesting**: Test storici su dati reali OANDA
- **Web Dashboard**: Interfaccia moderna per visualizzare segnali
- **REST API**: Endpoints completi per integrazione

### Quick Start

```bash
# 1. Installa dipendenze
pip install -r requirements.txt

# 2. Configura OANDA API
cp .env.example .env
# Modifica .env con le tue credenziali OANDA

# 3. Avvia web app
python app.py

# 4. Apri browser
http://localhost:5000
```

### Documentazione Completa

Vedi **[README_FOREX.md](README_FOREX.md)** per:
- Installazione dettagliata (incluso TA-Lib)
- Guida API OANDA
- Esempi di utilizzo
- Strategie trading consigliate
- API Reference completa

### Demo Rapida

```python
# Esegui esempi
python example.py
```

### Stack Tecnologico

- **Backend**: Python 3.8+, Flask
- **Analisi Tecnica**: pandas, TA-Lib, scipy
- **Dati**: OANDA API v20
- **Frontend**: HTML5, JavaScript vanilla
- **Deployment**: Docker ready

### Architettura

```
src/
├── oanda_client.py      # API OANDA integration
├── pattern_detector.py  # Candlestick patterns
├── support_resistance.py # S/R detection
├── scanner.py           # Multi-pair scanner
└── backtester.py        # Backtesting engine

app.py                   # Flask web app
templates/index.html     # Dashboard UI
```

### API Endpoints

- `GET /api/scan/<pair>` - Scansiona coppia forex
- `GET /api/scan/all` - Scansiona tutte le coppie
- `GET /api/signals` - Ottieni segnali attivi
- `POST /api/risk-calculator` - Calcola R/R
- E altri... (vedi README_FOREX.md)

### Strategia Implementata

**Price Action + Pattern Recognition**

1. Rileva pattern candlestick su timeframe H4/Daily
2. Verifica pattern su livelli chiave S/R
3. Calcola R/R automatico (minimo 1.5:1)
4. Genera segnali BUY/SELL con entry/stop/target

### Screenshot

![Dashboard](https://via.placeholder.com/800x400?text=Forex+Trading+Dashboard)

*(La dashboard mostra segnali in tempo reale con pattern, R/R e confidence level)*

### Roadmap

- [x] Pattern detection (Pin Bar, Engulfing, etc.)
- [x] Support/Resistance detection
- [x] Multi-pair scanner
- [x] Risk/Reward calculator
- [x] Backtesting engine
- [x] Web dashboard
- [ ] TradingView charts integration
- [ ] Telegram/Email alerts
- [ ] Machine Learning optimization
- [ ] Mobile app

### Disclaimer

**IMPORTANTE**: Questo software è fornito solo a scopo educativo. Il trading forex comporta rischi significativi. Non investire denaro che non puoi permetterti di perdere. Testa sempre su account demo.

### Supporto

Per domande o problemi, apri una issue su GitHub.

### Licenza

MIT

---

## Contatti

- GitHub: [occhim/betflag-bot](https://github.com/occhim/betflag-bot)
- Documentazione: README_FOREX.md
