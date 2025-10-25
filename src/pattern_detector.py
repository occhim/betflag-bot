"""
Candlestick Pattern Detection for Price Action Trading
"""
import pandas as pd
import numpy as np


class PatternDetector:
    """Detect candlestick patterns for price action trading"""

    def __init__(self, df):
        """
        Initialize pattern detector

        Args:
            df (pd.DataFrame): OHLC data
        """
        self.df = df.copy()
        self._calculate_candle_properties()

    def _calculate_candle_properties(self):
        """Calculate candle body, wicks, and ranges"""
        self.df['body'] = abs(self.df['close'] - self.df['open'])
        self.df['range'] = self.df['high'] - self.df['low']
        self.df['upper_wick'] = self.df['high'] - self.df[['open', 'close']].max(axis=1)
        self.df['lower_wick'] = self.df[['open', 'close']].min(axis=1) - self.df['low']
        self.df['body_position'] = (self.df['close'] - self.df['open']).apply(lambda x: 'bullish' if x > 0 else 'bearish')

    def detect_pin_bar(self, wick_ratio=2.0, body_ratio=0.3):
        """
        Detect Pin Bar / Hammer / Shooting Star

        Args:
            wick_ratio (float): Minimum ratio of wick to body
            body_ratio (float): Maximum body size relative to range

        Returns:
            pd.Series: Boolean series indicating pin bars
        """
        # Bullish Pin Bar (Hammer) - long lower wick
        bullish_pin = (
            (self.df['lower_wick'] >= self.df['body'] * wick_ratio) &
            (self.df['body'] <= self.df['range'] * body_ratio) &
            (self.df['upper_wick'] <= self.df['body'])
        )

        # Bearish Pin Bar (Shooting Star) - long upper wick
        bearish_pin = (
            (self.df['upper_wick'] >= self.df['body'] * wick_ratio) &
            (self.df['body'] <= self.df['range'] * body_ratio) &
            (self.df['lower_wick'] <= self.df['body'])
        )

        pin_bars = bullish_pin | bearish_pin
        self.df['pin_bar'] = pin_bars
        self.df['pin_bar_type'] = np.where(bullish_pin, 'bullish_hammer',
                                   np.where(bearish_pin, 'bearish_shooting_star', None))

        return pin_bars

    def detect_engulfing(self):
        """
        Detect Bullish/Bearish Engulfing patterns

        Returns:
            pd.Series: Boolean series indicating engulfing patterns
        """
        engulfing = pd.Series(False, index=self.df.index)
        engulfing_type = pd.Series(None, index=self.df.index)

        for i in range(1, len(self.df)):
            prev_body = self.df['body'].iloc[i-1]
            curr_body = self.df['body'].iloc[i]

            prev_open = self.df['open'].iloc[i-1]
            prev_close = self.df['close'].iloc[i-1]
            curr_open = self.df['open'].iloc[i]
            curr_close = self.df['close'].iloc[i]

            # Bullish Engulfing
            if (prev_close < prev_open and  # Previous bearish
                curr_close > curr_open and  # Current bullish
                curr_open <= prev_close and  # Opens at/below previous close
                curr_close >= prev_open):    # Closes at/above previous open
                engulfing.iloc[i] = True
                engulfing_type.iloc[i] = 'bullish_engulfing'

            # Bearish Engulfing
            elif (prev_close > prev_open and  # Previous bullish
                  curr_close < curr_open and  # Current bearish
                  curr_open >= prev_close and  # Opens at/above previous close
                  curr_close <= prev_open):    # Closes at/below previous open
                engulfing.iloc[i] = True
                engulfing_type.iloc[i] = 'bearish_engulfing'

        self.df['engulfing'] = engulfing
        self.df['engulfing_type'] = engulfing_type

        return engulfing

    def detect_inside_bar(self):
        """
        Detect Inside Bar patterns (consolidation)

        Returns:
            pd.Series: Boolean series indicating inside bars
        """
        inside_bars = pd.Series(False, index=self.df.index)

        for i in range(1, len(self.df)):
            prev_high = self.df['high'].iloc[i-1]
            prev_low = self.df['low'].iloc[i-1]
            curr_high = self.df['high'].iloc[i]
            curr_low = self.df['low'].iloc[i]

            # Current candle completely inside previous candle
            if curr_high <= prev_high and curr_low >= prev_low:
                inside_bars.iloc[i] = True

        self.df['inside_bar'] = inside_bars

        return inside_bars

    def detect_doji(self, body_ratio=0.1):
        """
        Detect Doji patterns (indecision)

        Args:
            body_ratio (float): Maximum body size relative to range

        Returns:
            pd.Series: Boolean series indicating dojis
        """
        dojis = self.df['body'] <= self.df['range'] * body_ratio
        self.df['doji'] = dojis

        return dojis

    def detect_morning_evening_star(self):
        """
        Detect Morning Star (bullish) and Evening Star (bearish) patterns

        Returns:
            pd.Series: Boolean series indicating star patterns
        """
        stars = pd.Series(False, index=self.df.index)
        star_type = pd.Series(None, index=self.df.index)

        for i in range(2, len(self.df)):
            candle1_open = self.df['open'].iloc[i-2]
            candle1_close = self.df['close'].iloc[i-2]
            candle2_body = self.df['body'].iloc[i-1]
            candle2_range = self.df['range'].iloc[i-1]
            candle3_open = self.df['open'].iloc[i]
            candle3_close = self.df['close'].iloc[i]

            # Morning Star (bullish reversal)
            if (candle1_close < candle1_open and  # First candle bearish
                candle2_body <= candle2_range * 0.3 and  # Second candle small (star)
                candle3_close > candle3_open and  # Third candle bullish
                candle3_close > (candle1_open + candle1_close) / 2):  # Closes above midpoint
                stars.iloc[i] = True
                star_type.iloc[i] = 'morning_star'

            # Evening Star (bearish reversal)
            elif (candle1_close > candle1_open and  # First candle bullish
                  candle2_body <= candle2_range * 0.3 and  # Second candle small (star)
                  candle3_close < candle3_open and  # Third candle bearish
                  candle3_close < (candle1_open + candle1_close) / 2):  # Closes below midpoint
                stars.iloc[i] = True
                star_type.iloc[i] = 'evening_star'

        self.df['star'] = stars
        self.df['star_type'] = star_type

        return stars

    def detect_all_patterns(self):
        """
        Detect all candlestick patterns

        Returns:
            pd.DataFrame: DataFrame with all patterns detected
        """
        self.detect_pin_bar()
        self.detect_engulfing()
        self.detect_inside_bar()
        self.detect_doji()
        self.detect_morning_evening_star()

        return self.df

    def get_recent_patterns(self, last_n=10):
        """
        Get recent detected patterns

        Args:
            last_n (int): Number of recent candles to check

        Returns:
            list: List of detected patterns
        """
        patterns = []
        recent_df = self.df.tail(last_n)

        for idx, row in recent_df.iterrows():
            pattern_info = {
                'time': idx,
                'patterns': []
            }

            if row.get('pin_bar', False):
                pattern_info['patterns'].append(row['pin_bar_type'])

            if row.get('engulfing', False):
                pattern_info['patterns'].append(row['engulfing_type'])

            if row.get('inside_bar', False):
                pattern_info['patterns'].append('inside_bar')

            if row.get('doji', False):
                pattern_info['patterns'].append('doji')

            if row.get('star', False):
                pattern_info['patterns'].append(row['star_type'])

            if pattern_info['patterns']:
                patterns.append(pattern_info)

        return patterns
