"""
Configuration settings for Forex Trading Analysis App
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""

    # OANDA API Settings
    OANDA_API_KEY = os.getenv('OANDA_API_KEY', '')
    OANDA_ACCOUNT_ID = os.getenv('OANDA_ACCOUNT_ID', '')
    OANDA_ENVIRONMENT = os.getenv('OANDA_ENVIRONMENT', 'practice')

    # OANDA API URLs
    OANDA_API_URL = {
        'practice': 'https://api-fxpractice.oanda.com',
        'live': 'https://api-fxtrade.oanda.com'
    }

    # Flask Settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    PORT = int(os.getenv('PORT', 5000))

    # Trading Settings
    DEFAULT_PAIRS = [
        'EUR_USD', 'GBP_USD', 'USD_JPY', 'USD_CHF',
        'AUD_USD', 'USD_CAD', 'NZD_USD'
    ]

    # Timeframes for multi-timeframe analysis
    TIMEFRAMES = ['H1', 'H4', 'D']

    # Pattern detection settings
    MIN_CANDLES_FOR_PATTERN = 50  # Minimum candles to analyze
    SUPPORT_RESISTANCE_LOOKBACK = 100  # Candles to look back for S/R
    SUPPORT_RESISTANCE_TOLERANCE = 0.0005  # 5 pips tolerance

    # Risk Management
    DEFAULT_RISK_PERCENT = 1.0  # 1% risk per trade
    MIN_RISK_REWARD = 1.5  # Minimum 1:1.5 R/R ratio
