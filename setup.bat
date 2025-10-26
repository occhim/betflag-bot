@echo off
REM Forex Trading Analysis App - Setup Automatico (Windows)
REM Script per installazione e configurazione automatica

color 0B
echo.
echo ========================================================
echo    Forex Trading Analysis App - Setup
echo    Installazione Automatica (Windows)
echo ========================================================
echo.

REM 1. Verifica Python
echo [STEP] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python non trovato!
    echo.
    echo Scarica e installa Python da:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante installazione, spunta "Add Python to PATH"
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% trovato
echo.

REM 2. Verifica pip
echo [STEP] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] pip non trovato!
    echo.
    echo Reinstalla Python assicurandoti di includere pip
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('pip --version 2^>^&1') do set PIP_VERSION=%%i
echo [OK] pip %PIP_VERSION% trovato
echo.

REM 3. Crea virtual environment
echo [STEP] Creando virtual environment...
if exist venv (
    echo [!] Virtual environment gia esistente. Skip.
) else (
    python -m venv venv
    echo [OK] Virtual environment creato
)
echo.

REM 4. Attiva virtual environment
echo [STEP] Attivando virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment attivo
echo.

REM 5. Aggiorna pip
echo [STEP] Aggiornando pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo [OK] pip aggiornato
echo.

REM 6. TA-Lib warning
echo [STEP] Verificando TA-Lib...
python -c "import talib" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] TA-Lib non installato
    echo.
    echo TA-Lib richiede installazione manuale su Windows:
    echo.
    echo OPZIONE 1 - File Pre-compilato (CONSIGLIATO):
    echo 1. Vai su: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
    echo 2. Scarica il file .whl per la tua versione Python
    echo    (es. TA_Lib-0.4.28-cp311-cp311-win_amd64.whl per Python 3.11)
    echo 3. Installa con: pip install NOME_FILE.whl
    echo.
    echo OPZIONE 2 - Libreria Alternativa:
    echo pip install ta
    echo.
    echo Per ora proseguo con l'installazione delle altre dipendenze...
    timeout /t 5
) else (
    echo [OK] TA-Lib gia installato
)
echo.

REM 7. Installa dipendenze Python
echo [STEP] Installando dipendenze Python (2-5 minuti)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [X] Errore durante installazione dipendenze
    echo.
    echo Prova:
    echo 1. Aggiorna pip: python -m pip install --upgrade pip
    echo 2. Riprova: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Dipendenze installate
echo.

REM 8. Configura .env
echo [STEP] Configurando file .env...
if exist .env (
    echo [!] File .env gia esistente. Skip.
) else (
    copy .env.example .env >nul
    echo [OK] File .env creato da .env.example
    echo.
    echo [!] IMPORTANTE: Modifica .env con le tue credenziali OANDA!
)
echo.

REM 9. Test installazione
echo [STEP] Testando installazione...
python -c "import pandas; import flask; import oandapyV20" >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Test import moduli: FAILED
    pause
    exit /b 1
)
echo [OK] Test import moduli: OK
echo.

REM 10. Riepilogo
echo.
echo ========================================================
echo    Setup Completato!
echo ========================================================
echo.
echo Prossimi Passi:
echo.
echo 1. Configura OANDA API:
echo    notepad .env
echo    Modifica OANDA_API_KEY e OANDA_ACCOUNT_ID
echo.
echo 2. Se TA-Lib non installato, segui istruzioni sopra
echo.
echo 3. Esegui esempi:
echo    python example.py
echo.
echo 4. Avvia web app:
echo    python app.py
echo    Poi apri: http://localhost:5000
echo.
echo 5. Leggi documentazione:
echo    notepad SETUP_GUIDE.md
echo.
echo [!] Ricorda di attivare virtual environment ad ogni sessione:
echo    venv\Scripts\activate
echo.
echo Buon Trading!
echo.

pause
