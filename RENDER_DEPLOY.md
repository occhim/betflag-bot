# Deploy su Render.com - Guida Completa

Guida passo-passo per fare il deploy dell'app Forex Trading Analysis su Render.com e usarla da iPhone.

---

## 📋 Prerequisiti

- ✅ Account Render.com (hai già)
- ✅ Account GitHub con il repository
- ✅ Account OANDA demo (per API key)

---

## 🚀 Passo 1: Push dei File di Deploy

I file necessari sono già stati creati:
- `Dockerfile` - Container configuration
- `render.yaml` - Render configuration
- `.dockerignore` - File da escludere
- `requirements.txt` - Dipendenze aggiornate

**Questi file sono già nel repository dopo il merge della PR.**

---

## 🔗 Passo 2: Connetti GitHub a Render

### 2.1 Login su Render
1. Vai su: https://render.com/
2. Clicca **"Dashboard"** (dovresti essere già loggato)

### 2.2 Crea Nuovo Web Service
1. Clicca **"New +"** (in alto a destra)
2. Seleziona **"Web Service"**

### 2.3 Connetti Repository
Se è la prima volta:
```
1. Clicca "Connect account" sotto GitHub
2. Autorizza Render ad accedere a GitHub
3. Seleziona "All repositories" o solo "betflag-bot"
4. Clicca "Install"
```

Se hai già connesso GitHub:
```
1. Cerca "betflag-bot" nella lista
2. Clicca "Connect" accanto al repository
```

---

## ⚙️ Passo 3: Configura il Web Service

Render mostrerà un form di configurazione:

### 3.1 Informazioni Base

| Campo | Valore |
|-------|--------|
| **Name** | `forex-trading-app` (o nome a tua scelta) |
| **Region** | `Frankfurt (EU Central)` (più vicino all'Italia) |
| **Branch** | `main` |
| **Root Directory** | (lascia vuoto) |
| **Environment** | `Docker` |
| **Instance Type** | `Free` |

### 3.2 Build & Deploy

Render dovrebbe rilevare automaticamente il `Dockerfile`. Verifica:

| Campo | Valore |
|-------|--------|
| **Dockerfile Path** | `./Dockerfile` |
| **Docker Context** | `.` |

---

## 🔐 Passo 4: Configura Variabili d'Ambiente

**IMPORTANTE**: Qui inserisci le tue credenziali OANDA!

Scorri fino alla sezione **"Environment Variables"**

### 4.1 Aggiungi Variabili

Clicca **"Add Environment Variable"** per ognuna:

#### Variabile 1: OANDA_API_KEY
```
Key:   OANDA_API_KEY
Value: [IL_TUO_API_TOKEN_OANDA]
```
Esempio: `1a2b3c4d5e6f7g8h9i0j-abcdefghijklmnop`

#### Variabile 2: OANDA_ACCOUNT_ID
```
Key:   OANDA_ACCOUNT_ID
Value: [IL_TUO_ACCOUNT_ID_OANDA]
```
Esempio: `101-001-1234567-001`

#### Variabile 3: OANDA_ENVIRONMENT
```
Key:   OANDA_ENVIRONMENT
Value: practice
```

#### Variabile 4: FLASK_ENV
```
Key:   FLASK_ENV
Value: production
```

#### Variabile 5: FLASK_DEBUG
```
Key:   FLASK_DEBUG
Value: False
```

**Totale: 5 variabili d'ambiente**

---

## 🎯 Passo 5: Avvia il Deploy

1. Verifica tutte le impostazioni
2. Scorri in basso
3. Clicca **"Create Web Service"** (bottone blu)

Render inizierà il build e deploy automaticamente!

---

## ⏱️ Passo 6: Attendi il Deploy (5-10 minuti)

### 6.1 Cosa Succede

Vedrai i log in tempo reale:

```
==> Cloning from GitHub...
==> Building Docker image...
==> Installing TA-Lib...
==> Installing Python dependencies...
==> Starting application...
==> Your service is live 🎉
```

**Tempo stimato**: 5-10 minuti (TA-Lib richiede compilazione)

### 6.2 Controlla Status

In alto vedrai lo status:
- 🔄 **Building** - In costruzione
- 🟡 **Deploying** - Deployment in corso
- 🟢 **Live** - Online e funzionante! ✅

### 6.3 Se Ci Sono Errori

Se vedi 🔴 **Failed**:
1. Clicca su **"Logs"** per vedere l'errore
2. Problemi comuni:
   - TA-Lib compilation failed → Riprova deploy (a volte timeout)
   - Missing env variables → Controlla variabili d'ambiente
   - Port binding error → Verifica Dockerfile

---

## 🌐 Passo 7: Ottieni URL dell'App

### 7.1 Trova l'URL

Una volta che lo status è 🟢 **Live**:

1. In alto vedrai l'URL pubblico:
   ```
   https://forex-trading-app-XXXX.onrender.com
   ```
   (XXXX è un ID univoco)

2. **Copia questo URL!**

### 7.2 Testa l'App

**Da computer:**
```bash
# Test health check
curl https://TUO_URL.onrender.com/api/health

# Dovresti vedere:
# {"status":"healthy","version":"1.0.0","api_configured":true}
```

**Da browser:**
```
Apri: https://TUO_URL.onrender.com
```

Dovresti vedere la dashboard!

---

## 📱 Passo 8: Usa l'App da iPhone

### 8.1 Apri Safari su iPhone

1. Apri **Safari**
2. Vai su: `https://TUO_URL.onrender.com`
3. La dashboard si apre!

### 8.2 Aggiungi alla Home Screen (CONSIGLIATO)

Per usarla come app nativa:

```
1. Clicca l'icona "Condividi" (quadrato con freccia)
2. Scorri e clicca "Aggiungi a Home"
3. Personalizza nome: "Forex Signals"
4. Clicca "Aggiungi"
```

Ora hai un'icona sulla home screen che apre l'app a schermo intero!

### 8.3 Usa l'App

1. **Apri l'app** dall'icona home
2. **Clicca "Scan All Pairs"**
3. **Attendi 10-30 secondi**
4. **Vedi segnali BUY/SELL!**

---

## 🔄 Auto-Deploy (Bonus)

Render fa auto-deploy ad ogni push su GitHub!

**Come funziona:**
```
1. Modifichi codice localmente
2. git commit + git push
3. Render rileva il push
4. Rebuild automatico
5. App aggiornata in 5-10 minuti
```

Per disattivare auto-deploy:
```
Settings → Build & Deploy → Auto-Deploy: OFF
```

---

## 📊 Monitoraggio

### Dashboard Render

**Metrics:**
- CPU Usage
- Memory Usage
- Request count
- Response time

**Logs:**
- Real-time application logs
- Error tracking

**Eventi:**
- Deploy history
- Uptime status

---

## 💰 Piano Free Render

### Limiti
- ✅ 750 ore/mese (circa 31 giorni)
- ✅ 512MB RAM
- ✅ Shared CPU
- ⚠️ App va in sleep dopo 15 min inattività
- ⚠️ Primo request dopo sleep: ~30 sec

### Cosa Significa "Sleep"

Se non usi l'app per 15 minuti:
- Render mette in sleep il container
- Primo accesso successivo: lento (~30 sec)
- Request successivi: veloci

**Soluzione**: Upgrade a piano $7/mese (sempre attivo)

---

## 🔧 Troubleshooting

### ❌ Build Failed - TA-Lib Error

**Problema**: Compilazione TA-Lib fallisce

**Soluzione**:
```
1. Vai su Render Dashboard
2. Clicca "Manual Deploy" → "Clear build cache & deploy"
3. Riprova
```

Se ancora fallisce:
```
1. Modifica requirements.txt
2. Commenta: # ta-lib==0.4.28
3. Mantieni: ta==0.11.0 (libreria alternativa)
4. Push su GitHub
```

### ❌ "Unauthorized" API Error

**Problema**: API OANDA non funziona

**Soluzione**:
```
1. Render Dashboard → tua app
2. Environment → Edit
3. Verifica OANDA_API_KEY e OANDA_ACCOUNT_ID
4. Salva
5. Clicca "Manual Deploy" → "Deploy latest commit"
```

### ❌ App Lenta / Timeout

**Problema**: First request lento dopo sleep

**Soluzione**:
```
Opzione A: Aspetta 30 sec al primo accesso
Opzione B: Upgrade a piano $7/mese (no sleep)
Opzione C: Usa servizio come UptimeRobot per ping ogni 14 min
```

### ❌ Dashboard Non Si Carica

**Problema**: Pagina bianca o errore

**Soluzione**:
```
1. Controlla Logs su Render
2. Verifica che sia in stato "Live"
3. Prova /api/health endpoint
4. Controlla variabili d'ambiente
```

---

## 📱 Test dell'App da iPhone

### Cosa Testare

1. **Health Check**
   ```
   Apri: https://TUO_URL.onrender.com/api/health
   Dovresti vedere: {"status":"healthy",...}
   ```

2. **Dashboard**
   ```
   Apri: https://TUO_URL.onrender.com
   Dovresti vedere: interfaccia con controlli
   ```

3. **Scan Pairs**
   ```
   Clicca "Scan All Pairs"
   Attendi 20-30 secondi
   Dovresti vedere: cards con segnali
   ```

4. **Active Signals**
   ```
   Clicca "Get Active Signals"
   Dovresti vedere: segnali BUY/SELL filtrati
   ```

---

## 🎯 Checklist Deploy Completo

Prima di usare l'app, verifica:

- [ ] Repository connesso a Render
- [ ] Docker environment selezionato
- [ ] 5 variabili d'ambiente configurate
- [ ] Build completato con successo
- [ ] Status: 🟢 Live
- [ ] URL pubblico ottenuto
- [ ] Dashboard si apre da browser
- [ ] /api/health risponde con status:healthy
- [ ] Scan funziona e mostra segnali
- [ ] App aggiunta a Home Screen iPhone
- [ ] Test completo da iPhone OK

**Se tutti ✅ sei pronto!** 🎉

---

## 🆘 Serve Aiuto?

### Link Utili
- **Render Docs**: https://render.com/docs
- **Render Support**: https://render.com/support
- **OANDA API Docs**: https://developer.oanda.com/

### Problemi Comuni
1. Leggi sezione Troubleshooting sopra
2. Controlla Logs su Render Dashboard
3. Verifica variabili d'ambiente
4. Riprova deploy con "Clear build cache"

---

## 🎉 Complimenti!

Una volta completato il deploy:

✅ App forex online 24/7
✅ Accessibile da qualsiasi dispositivo
✅ URL pubblico condivisibile
✅ Auto-deploy ad ogni push GitHub
✅ Usabile da iPhone come app nativa

---

**Segui i passi sopra e dimmi se hai problemi!** 🚀

La tua app sarà live in 10-15 minuti.
