# Alpha Vantage Setup - Guida Veloce

Alpha Vantage è un'alternativa **gratuita** e **semplice** a OANDA per ottenere dati forex.

---

## ✅ Vantaggi Alpha Vantage

- **100% Gratuito**
- **Setup in 2 minuti** (solo email)
- **API key istantanea** (nessuna verifica documento)
- **25 richieste/giorno** (sufficiente per 3-5 scansioni)
- **Stessa qualità dati** forex real-time

---

## 🚀 STEP 1: Ottieni API Key (2 minuti)

### **1.1 Vai sul sito Alpha Vantage**

```
https://www.alphavantage.co/support/#api-key
```

### **1.2 Inserisci la tua email**

- Scrivi la tua email nel campo
- Clicca **"GET FREE API KEY"**

### **1.3 Copia l'API Key**

Vedrai immediatamente la tua API key:

```
Your API Key: ABCDEF123456
```

**COPIA questo codice!** ✅

---

## ⚙️ STEP 2: Configura su Render

### **2.1 Vai su Render Dashboard**

```
https://dashboard.render.com
```

### **2.2 Apri la tua app**

Clicca su **"forex-trading-app"**

### **2.3 Vai su Environment**

Nel menu a sinistra: **"Environment"**

### **2.4 Aggiungi/Modifica Variabili**

#### **Variabile 1: DATA_PROVIDER**

Se non esiste, clicca **"Add Environment Variable"**:

```
Key:   DATA_PROVIDER
Value: alphavantage
```

#### **Variabile 2: ALPHAVANTAGE_API_KEY**

```
Key:   ALPHAVANTAGE_API_KEY
Value: [INCOLLA LA TUA API KEY QUI]
```

Esempio: `ABCDEF123456`

#### **Variabile 3-5: Flask (se non già presenti)**

```
Key:   FLASK_ENV
Value: production

Key:   FLASK_DEBUG
Value: False
```

### **2.5 Salva e Riavvia**

1. **Clicca "Save Changes"** (in basso)
2. Render riavvierà automaticamente (30 secondi)

---

## ✅ STEP 3: Testa l'App

### **3.1 Aspetta il Riavvio**

Status diventa: 🟢 **Live**

### **3.2 Apri l'App da iPhone**

1. **Safari** → Apri il tuo URL Render
2. **Ricarica** la pagina
3. **Clicca "Scan All Pairs"**
4. **Attendi 20-30 secondi**

**VEDRAI I SEGNALI!** 🎉

---

## 📊 Cosa Aspettarsi

**Prima scansione:**
- Tempo: 30-60 secondi (sleep mode)
- Dati: Ultimi 500 candles per coppia
- Segnali: 3-8 pattern rilevati

**Scansioni successive:**
- Tempo: 10-20 secondi
- Sempre aggiornato

---

## 🎯 Limiti Alpha Vantage (Piano Free)

- ✅ **25 richieste/giorno**
- ✅ **5 richieste/minuto**

**Cosa significa?**

- Puoi fare **3-5 scansioni complete al giorno** (7 coppie forex)
- Ideale per: controllare mattina, pomeriggio, sera
- **Sufficiente** per trading non professionale

**Se hai bisogno di più:**
- Upgrade Alpha Vantage: $49/mese (unlimited)
- Oppure: Passa a OANDA (120 req/ora gratis)

---

## 🔄 Passare da Alpha Vantage a OANDA

Se in futuro vuoi passare a OANDA:

1. Registrati su OANDA
2. Su Render Environment:
   - Cambia `DATA_PROVIDER` da `alphavantage` a `oanda`
   - Aggiungi `OANDA_API_KEY` e `OANDA_ACCOUNT_ID`
3. Save Changes

**L'app supporta entrambi!** Puoi cambiare quando vuoi.

---

## 🆘 Troubleshooting

### ❌ "Note: API rate limit reached"

**Problema:** Hai usato le 25 richieste giornaliere

**Soluzione:**
- Aspetta domani (reset a mezzanotte UTC)
- Oppure usa OANDA (120 req/ora)

### ❌ "Error: Invalid API key"

**Problema:** API key errata

**Soluzione:**
1. Verifica su Render Environment
2. Controlla che `ALPHAVANTAGE_API_KEY` sia copiata correttamente
3. Nessuno spazio extra
4. Save Changes e riavvia

### ❌ "No data available"

**Problema:** Possibile timeout o coppia non supportata

**Soluzione:**
- Riprova dopo 1 minuto
- Verifica che la coppia sia major (EUR_USD, GBP_USD, etc.)

---

## 📋 Checklist Completa

- [ ] Vai su alphavantage.co
- [ ] Inserisci email
- [ ] Ricevi API key istantanea
- [ ] Copia API key
- [ ] Render → Environment
- [ ] Aggiungi `DATA_PROVIDER=alphavantage`
- [ ] Aggiungi `ALPHAVANTAGE_API_KEY=tuakey`
- [ ] Aggiungi `FLASK_ENV=production`
- [ ] Save Changes
- [ ] Aspetta riavvio (30 sec)
- [ ] Apri app da iPhone
- [ ] Scan All Pairs
- [ ] ✅ VEDI SEGNALI!

---

## 🎉 Vantaggi per Principianti

Alpha Vantage è **perfetto** se:

- ✅ Vuoi provare l'app **subito** (setup 2 minuti)
- ✅ Non vuoi registrarti con documenti
- ✅ Controlli i segnali **2-3 volte al giorno**
- ✅ Vuoi qualcosa di **gratuito al 100%**
- ✅ Stai **imparando** il trading

---

## 📚 Link Utili

- **Alpha Vantage**: https://www.alphavantage.co/
- **Documentazione API**: https://www.alphavantage.co/documentation/
- **Support**: support@alphavantage.co

---

**Setup completato in 2 minuti!** 🚀

Domande? Controlla la sezione Troubleshooting sopra!
