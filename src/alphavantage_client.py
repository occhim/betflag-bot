"""
Alpha Vantage API Client for forex data
Free alternative to OANDA - 25 requests/day
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
from config import Config


class AlphaVantageClient:
    """Client for Alpha Vantage API"""

    def __init__(self):
        """Initialize Alpha Vantage client"""
        self.api_key = Config.ALPHAVANTAGE_API_KEY
        self.base_url = "https://www.alphavantage.co/query"

    def _map_timeframe(self, granularity):
        """
        Map granularity to Alpha Vantage interval

        Args:
            granularity (str): Timeframe ('H1', 'H4', 'D')

        Returns:
            str: Alpha Vantage interval
        """
        mapping = {
            'H1': '60min',
            'H4': '60min',  # Resample to 4H
            'D': 'daily'
        }
        return mapping.get(granularity, '60min')

    def get_candles(self, instrument, granularity='H1', count=500):
        """
        Fetch candlestick data from Alpha Vantage

        Args:
            instrument (str): Forex pair (e.g., 'EUR_USD')
            granularity (str): Timeframe ('H1', 'H4', 'D')
            count (int): Number of candles to fetch

        Returns:
            pd.DataFrame: OHLCV data
        """
        try:
            # Convert instrument format: EUR_USD -> EURUSD
            from_currency = instrument.split('_')[0]
            to_currency = instrument.split('_')[1]

            # Determine function based on timeframe
            if granularity == 'D':
                function = 'FX_DAILY'
                params = {
                    'function': function,
                    'from_symbol': from_currency,
                    'to_symbol': to_currency,
                    'apikey': self.api_key,
                    'outputsize': 'full'  # Get more data
                }
            else:
                function = 'FX_INTRADAY'
                interval = self._map_timeframe(granularity)
                params = {
                    'function': function,
                    'from_symbol': from_currency,
                    'to_symbol': to_currency,
                    'interval': interval,
                    'apikey': self.api_key,
                    'outputsize': 'full'
                }

            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()

            # Check for errors
            if 'Error Message' in data:
                print(f"Alpha Vantage error: {data['Error Message']}")
                return None

            if 'Note' in data:
                print(f"Alpha Vantage rate limit: {data['Note']}")
                return None

            # Extract time series data
            if granularity == 'D':
                time_series_key = 'Time Series FX (Daily)'
            else:
                time_series_key = f'Time Series FX (60min)'

            if time_series_key not in data:
                print(f"No data found for {instrument}")
                return None

            time_series = data[time_series_key]

            # Convert to DataFrame
            df_data = []
            for timestamp, values in time_series.items():
                df_data.append({
                    'time': timestamp,
                    'open': float(values['1. open']),
                    'high': float(values['2. high']),
                    'low': float(values['3. low']),
                    'close': float(values['4. close']),
                    'volume': 0  # Alpha Vantage doesn't provide forex volume
                })

            df = pd.DataFrame(df_data)
            df['time'] = pd.to_datetime(df['time'])
            df = df.sort_values('time')
            df.set_index('time', inplace=True)

            # Resample to H4 if needed
            if granularity == 'H4':
                df = df.resample('4H').agg({
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'volume': 'sum'
                }).dropna()

            # Limit to requested count
            df = df.tail(count)

            return df

        except Exception as e:
            print(f"Error fetching candles for {instrument}: {str(e)}")
            return None

    def get_current_price(self, instrument):
        """
        Get current price for an instrument

        Args:
            instrument (str): Forex pair

        Returns:
            dict: Current bid/ask prices (simulated from latest close)
        """
        try:
            # Convert instrument format
            from_currency = instrument.split('_')[0]
            to_currency = instrument.split('_')[1]

            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': from_currency,
                'to_currency': to_currency,
                'apikey': self.api_key
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()

            if 'Realtime Currency Exchange Rate' in data:
                rate_data = data['Realtime Currency Exchange Rate']
                price = float(rate_data['5. Exchange Rate'])

                # Simulate bid/ask with small spread (0.0002 = 2 pips)
                spread = 0.0002
                return {
                    'bid': price - spread / 2,
                    'ask': price + spread / 2,
                    'spread': spread
                }

            return None

        except Exception as e:
            print(f"Error fetching price for {instrument}: {str(e)}")
            return None
