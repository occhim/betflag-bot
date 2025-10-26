# Forex Trading Analysis App

**Price Action & Pattern Recognition System** per il trading forex.

Un'applicazione completa per l'analisi tecnica basata su **Price Action** e riconoscimento automatico di pattern candlestick.

---

## Caratteristiche Principali

### Pattern Candlestick Rilevati
- **Pin Bar** (Hammer / Shooting Star)
- **Engulfing** (Bullish / Bearish)
- **Inside Bar** (consolidamento)
- **Doji** (indecisione)
- **Morning Star** (inversione rialzista)
- **Evening Star** (inversione ribassista)

### Analisi Supporti/Resistenze
- Rilevamento automatico di livelli chiave
- Clustering di pivot points
- Calcolo forza dei livelli (numero di tocchi)
- Livelli più vicini al prezzo corrente

### Scanner Multi-Coppia
- Scansione simultanea di 7 coppie forex major
- Analisi multi-timeframe (H1, H4, Daily)
- Generazione segnali BUY/SELL automatici
- Filtro per pattern su livelli chiave

### Risk Management
- Calcolo automatico Risk/Reward
- Calcolo position size basato su % di rischio
- Stop Loss e Take Profit automatici su livelli S/R
- Validazione ratio R/R minimo (default 1.5:1)

### Backtesting
- Test storico dell'accuratezza dei pattern
- Statistiche complete (Win Rate, Profit Factor, Drawdown)
- Test su dati reali OANDA

### Web Dashboard
- Interfaccia web moderna e responsive
- Visualizzazione segnali in tempo reale
- Statistiche aggregate
- API REST completa

---

## Installazione

### 1. Requisiti
- Python 3.8+
- Account OANDA (demo gratuito)

### 2. Clone del repository
```bash
git clone <repository-url>
cd betflag-bot
```

### 3. Installazione dipendenze

**IMPORTANTE**: TA-Lib richiede installazione nativa prima del pip install

#### Su Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y build-essential wget
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz
```

#### Su macOS:
```bash
brew install ta-lib
```

#### Su Windows:
Scarica i binari pre-compilati da:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

Poi installa con:
```bash
pip install TA_Lib-0.4.XX-cpXX-cpXX-win_amd64.whl
```

### 4. Installa dipendenze Python
```bash
pip install -r requirements.txt
```

### 5. Configurazione API OANDA

1. Registrati su OANDA (account practice gratuito):
   https://www.oanda.com/

2. Crea un API Token:
   - Vai su **Manage API Access**
   - Genera un nuovo token
   - Copia il token e l'account ID

3. Crea file `.env`:
```bash
cp .env.example .env
```

4. Modifica `.env`:
```bash
OANDA_API_KEY=your_api_key_here
OANDA_ACCOUNT_ID=your_account_id_here
OANDA_ENVIRONMENT=practice
```

---

## Utilizzo

### Avvio Web App

```bash
python app.py
```

Apri browser su: **http://localhost:5000**

### API Endpoints

#### 1. Health Check
```bash
GET /api/health
```

#### 2. Scansione singola coppia
```bash
GET /api/scan/EUR_USD?timeframe=H4
```

#### 3. Scansione tutte le coppie
```bash
GET /api/scan/all?timeframe=H4
```

#### 4. Analisi multi-timeframe
```bash
GET /api/scan/multi-timeframe/EUR_USD
```

#### 5. Segnali attivi
```bash
GET /api/signals?timeframe=H4
```

#### 6. Prezzo corrente
```bash
GET /api/price/EUR_USD
```

#### 7. Calcolo Risk/Reward
```bash
POST /api/risk-calculator
Content-Type: application/json

{
  "pair": "EUR_USD",
  "entry": 1.1000,
  "direction": "long",
  "stop_loss_pips": 20,
  "take_profit_pips": 40,
  "account_size": 10000,
  "risk_percent": 1
}
```

---

## Utilizzo Programmatico

### Scanner

```python
from src.scanner import ForexScanner

scanner = ForexScanner()

# Scansiona una coppia
result = scanner.scan_pair('EUR_USD', timeframe='H4')
print(result)

# Scansiona tutte le coppie
results = scanner.scan_all_pairs(timeframe='H4')

# Ottieni solo segnali attivi
signals = scanner.get_active_signals(timeframe='H4')
for signal in signals:
    print(f"{signal['pair']}: {signal['type']} - {signal['reason']}")
```

### Pattern Detection

```python
from src.oanda_client import OandaClient
from src.pattern_detector import PatternDetector

# Ottieni dati
client = OandaClient()
df = client.get_candles('EUR_USD', granularity='H4', count=500)

# Rileva pattern
detector = PatternDetector(df)
detector.detect_all_patterns()

# Ottieni pattern recenti
recent = detector.get_recent_patterns(last_n=10)
print(recent)
```

### Support/Resistance

```python
from src.support_resistance import SupportResistance

sr = SupportResistance(df)
levels = sr.detect_support_resistance()

print("Support levels:", levels['support'])
print("Resistance levels:", levels['resistance'])

# Calcola R/R per un trade
current_price = 1.1000
rr = sr.calculate_risk_reward(current_price, 'long')
print(f"Entry: {rr['entry']}")
print(f"Stop: {rr['stop_loss']}")
print(f"Target: {rr['take_profit']}")
print(f"R/R: 1:{rr['risk_reward_ratio']}")
```

### Backtesting

```python
from src.backtester import Backtester
from src.oanda_client import OandaClient

# Ottieni dati storici
client = OandaClient()
df = client.get_candles('EUR_USD', granularity='H4', count=5000)

# Backtest
backtester = Backtester(initial_balance=10000, risk_per_trade=1.0)
results = backtester.backtest_pattern(df, 'pin_bar', direction='both', min_rr=1.5)

print(f"Total Trades: {results['total_trades']}")
print(f"Win Rate: {results['win_rate']}%")
print(f"Total Return: {results['total_return']}%")
print(f"Profit Factor: {results['profit_factor']}")
print(f"Max Drawdown: {results['max_drawdown']}%")
```

---

## Strategia Trading Consigliata

### Regole di Entry

1. **Pattern candlestick** su livello chiave (S/R)
2. **Timeframe H4 o Daily** per affidabilità
3. **R/R minimo 1.5:1**
4. **Conferma multi-timeframe** (opzionale ma consigliato)

### Esempio Trade LONG

```
✅ Pin Bar bullish (Hammer) su supporto H4
✅ RSI < 40 (ipervenduto)
✅ R/R 1:2
✅ Trend Daily rialzista

Entry: 1.1000
Stop: 1.0980 (20 pips - sotto supporto)
Target: 1.1040 (40 pips - resistenza successiva)
Risk: 1% account
```

### Money Management

- **Mai rischiare più del 2% per trade**
- **Position size calcolato automaticamente**
- **Stop loss sempre attivo**
- **Massimo 3-5 trade aperti contemporaneamente**

---

## Struttura Progetto

```
betflag-bot/
├── app.py                    # Flask web app
├── config.py                 # Configurazione
├── requirements.txt          # Dipendenze
├── .env                      # API keys (non committare!)
├── src/
│   ├── __init__.py
│   ├── oanda_client.py      # Client API OANDA
│   ├── pattern_detector.py  # Rilevamento pattern
│   ├── support_resistance.py # S/R detection
│   ├── scanner.py           # Multi-pair scanner
│   └── backtester.py        # Backtesting engine
└── templates/
    └── index.html           # Web dashboard
```

---

## Configurazione Avanzata

### config.py

```python
# Coppie forex da scansionare
DEFAULT_PAIRS = [
    'EUR_USD', 'GBP_USD', 'USD_JPY', 'USD_CHF',
    'AUD_USD', 'USD_CAD', 'NZD_USD'
]

# Timeframe per analisi multi-TF
TIMEFRAMES = ['H1', 'H4', 'D']

# Parametri pattern detection
MIN_CANDLES_FOR_PATTERN = 50
SUPPORT_RESISTANCE_LOOKBACK = 100
SUPPORT_RESISTANCE_TOLERANCE = 0.0005  # 5 pips

# Risk management
DEFAULT_RISK_PERCENT = 1.0
MIN_RISK_REWARD = 1.5
```

---

## Limitazioni & Note

1. **API OANDA practice** è gratuita ma ha limiti di rate (120 req/ora)
2. **TA-Lib** richiede installazione nativa (vedi sopra)
3. **Pattern recognition** non è garanzia di profitto - usa sempre risk management
4. **Backtesting** usa dati storici - performance passate non garantiscono risultati futuri
5. **Spread e commissioni** non sono considerati nel backtest di base

---

## Prossimi Sviluppi

- [ ] Integrazione TradingView charts
- [ ] Alert via Telegram/Email
- [ ] Machine Learning per ottimizzazione pattern
- [ ] Automazione ordini (con conferma manuale)
- [ ] Analisi sentiment news
- [ ] Mobile app iOS/Android

---

## Supporto & Contributi

Per domande, bug o feature request, apri una issue su GitHub.

---

## Disclaimer

**IMPORTANTE**: Questo software è fornito solo a scopo educativo. Il trading forex comporta rischi significativi di perdita. Non investire denaro che non puoi permetterti di perdere. Gli sviluppatori non sono responsabili per eventuali perdite finanziarie derivanti dall'uso di questo software.

**Testa sempre su account demo prima di usare denaro reale.**

---

## Licenza

MIT License - vedi file LICENSE

---

## Risorse Utili

- [OANDA API Documentation](https://developer.oanda.com/rest-live-v20/introduction/)
- [Price Action Trading Guide](https://www.babypips.com/learn/forex/price-action)
- [TA-Lib Documentation](https://ta-lib.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Made with ❤️ for forex traders**
