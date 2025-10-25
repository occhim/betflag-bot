"""
OANDA API Client for fetching forex data
"""
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from datetime import datetime, timedelta
from config import Config


class OandaClient:
    """Client for interacting with OANDA API"""

    def __init__(self):
        """Initialize OANDA client"""
        self.api_key = Config.OANDA_API_KEY
        self.account_id = Config.OANDA_ACCOUNT_ID
        self.environment = Config.OANDA_ENVIRONMENT

        # Initialize OANDA API client
        self.client = oandapyV20.API(
            access_token=self.api_key,
            environment=self.environment
        )

    def get_candles(self, instrument, granularity='H1', count=500):
        """
        Fetch candlestick data from OANDA

        Args:
            instrument (str): Forex pair (e.g., 'EUR_USD')
            granularity (str): Timeframe ('M15', 'H1', 'H4', 'D')
            count (int): Number of candles to fetch (max 5000)

        Returns:
            pd.DataFrame: OHLCV data
        """
        params = {
            'granularity': granularity,
            'count': count,
            'price': 'M'  # Mid prices
        }

        try:
            request = instruments.InstrumentsCandles(
                instrument=instrument,
                params=params
            )

            response = self.client.request(request)

            # Convert to DataFrame
            candles = response.get('candles', [])

            data = []
            for candle in candles:
                if candle['complete']:
                    data.append({
                        'time': candle['time'],
                        'open': float(candle['mid']['o']),
                        'high': float(candle['mid']['h']),
                        'low': float(candle['mid']['l']),
                        'close': float(candle['mid']['c']),
                        'volume': int(candle['volume'])
                    })

            df = pd.DataFrame(data)
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)

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
            dict: Current bid/ask prices
        """
        try:
            request = instruments.InstrumentsPricing(
                accountID=self.account_id,
                params={'instruments': instrument}
            )

            response = self.client.request(request)
            prices = response.get('prices', [])

            if prices:
                price = prices[0]
                return {
                    'bid': float(price['bids'][0]['price']),
                    'ask': float(price['asks'][0]['price']),
                    'spread': float(price['asks'][0]['price']) - float(price['bids'][0]['price'])
                }

            return None

        except Exception as e:
            print(f"Error fetching price for {instrument}: {str(e)}")
            return None
