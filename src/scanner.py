"""
Multi-pair Pattern Scanner for Forex
"""
from src.oanda_client import OandaClient
from src.pattern_detector import PatternDetector
from src.support_resistance import SupportResistance
from config import Config
import pandas as pd
from datetime import datetime


class ForexScanner:
    """Scanner for detecting price action patterns across multiple pairs"""

    def __init__(self):
        """Initialize scanner"""
        self.client = OandaClient()
        self.pairs = Config.DEFAULT_PAIRS
        self.timeframes = Config.TIMEFRAMES

    def scan_pair(self, pair, timeframe='H4'):
        """
        Scan single pair for patterns

        Args:
            pair (str): Forex pair (e.g., 'EUR_USD')
            timeframe (str): Timeframe to analyze

        Returns:
            dict: Scan results
        """
        try:
            # Fetch data
            df = self.client.get_candles(pair, granularity=timeframe, count=200)

            if df is None or df.empty:
                return {
                    'pair': pair,
                    'timeframe': timeframe,
                    'error': 'No data available'
                }

            # Detect patterns
            pattern_detector = PatternDetector(df)
            pattern_detector.detect_all_patterns()

            # Detect support/resistance
            sr_detector = SupportResistance(df)
            levels = sr_detector.detect_support_resistance()

            # Get current price
            current_price_data = self.client.get_current_price(pair)
            current_price = current_price_data['bid'] if current_price_data else df['close'].iloc[-1]

            # Get recent patterns
            recent_patterns = pattern_detector.get_recent_patterns(last_n=5)

            # Get nearest levels
            nearest_levels = sr_detector.get_nearest_levels(current_price)

            # Check if at key level
            at_level = sr_detector.is_at_level(current_price)

            # Latest candle info
            latest_candle = df.iloc[-1]

            result = {
                'pair': pair,
                'timeframe': timeframe,
                'timestamp': datetime.now().isoformat(),
                'current_price': round(current_price, 5),
                'spread': current_price_data['spread'] if current_price_data else None,
                'recent_patterns': recent_patterns,
                'support_levels': levels['support'][:5],  # Top 5
                'resistance_levels': levels['resistance'][:5],  # Top 5
                'nearest_support': nearest_levels['support'],
                'nearest_resistance': nearest_levels['resistance'],
                'at_key_level': at_level['at_support'] or at_level['at_resistance'],
                'level_info': at_level,
                'latest_candle': {
                    'open': float(latest_candle['open']),
                    'high': float(latest_candle['high']),
                    'low': float(latest_candle['low']),
                    'close': float(latest_candle['close']),
                    'body_position': latest_candle.get('body_position', 'neutral')
                }
            }

            # Generate signals
            result['signals'] = self._generate_signals(result, pattern_detector, sr_detector)

            return result

        except Exception as e:
            return {
                'pair': pair,
                'timeframe': timeframe,
                'error': str(e)
            }

    def _generate_signals(self, scan_result, pattern_detector, sr_detector):
        """
        Generate trading signals based on patterns and levels

        Args:
            scan_result (dict): Scan results
            pattern_detector (PatternDetector): Pattern detector instance
            sr_detector (SupportResistance): S/R detector instance

        Returns:
            list: Trading signals
        """
        signals = []
        current_price = scan_result['current_price']
        recent_patterns = scan_result['recent_patterns']

        if not recent_patterns:
            return signals

        # Get latest pattern
        latest_pattern_info = recent_patterns[-1]

        for pattern in latest_pattern_info['patterns']:
            signal = None

            # Bullish patterns
            if pattern in ['bullish_hammer', 'bullish_engulfing', 'morning_star']:
                # Check if at support level
                if scan_result['level_info']['at_support']:
                    rr = sr_detector.calculate_risk_reward(current_price, 'long')
                    if rr['risk_reward_ratio'] >= Config.MIN_RISK_REWARD:
                        signal = {
                            'type': 'BUY',
                            'pattern': pattern,
                            'reason': f"{pattern} at support level",
                            'confidence': 'HIGH',
                            'entry': current_price,
                            'stop_loss': rr['stop_loss'],
                            'take_profit': rr['take_profit'],
                            'risk_reward': rr['risk_reward_ratio'],
                            'risk_pips': rr['risk_pips'],
                            'reward_pips': rr['reward_pips']
                        }

            # Bearish patterns
            elif pattern in ['bearish_shooting_star', 'bearish_engulfing', 'evening_star']:
                # Check if at resistance level
                if scan_result['level_info']['at_resistance']:
                    rr = sr_detector.calculate_risk_reward(current_price, 'short')
                    if rr['risk_reward_ratio'] >= Config.MIN_RISK_REWARD:
                        signal = {
                            'type': 'SELL',
                            'pattern': pattern,
                            'reason': f"{pattern} at resistance level",
                            'confidence': 'HIGH',
                            'entry': current_price,
                            'stop_loss': rr['stop_loss'],
                            'take_profit': rr['take_profit'],
                            'risk_reward': rr['risk_reward_ratio'],
                            'risk_pips': rr['risk_pips'],
                            'reward_pips': rr['reward_pips']
                        }

            # Inside bar breakout potential
            elif pattern == 'inside_bar':
                signal = {
                    'type': 'WATCH',
                    'pattern': pattern,
                    'reason': 'Consolidation - potential breakout',
                    'confidence': 'MEDIUM',
                    'action': 'Wait for breakout direction'
                }

            # Doji indecision
            elif pattern == 'doji':
                signal = {
                    'type': 'WATCH',
                    'pattern': pattern,
                    'reason': 'Indecision - potential reversal',
                    'confidence': 'LOW',
                    'action': 'Wait for confirmation'
                }

            if signal:
                signals.append(signal)

        return signals

    def scan_all_pairs(self, timeframe='H4'):
        """
        Scan all configured pairs

        Args:
            timeframe (str): Timeframe to analyze

        Returns:
            list: Results for all pairs
        """
        results = []

        for pair in self.pairs:
            print(f"Scanning {pair} on {timeframe}...")
            result = self.scan_pair(pair, timeframe)
            results.append(result)

        return results

    def scan_multi_timeframe(self, pair):
        """
        Scan single pair across multiple timeframes

        Args:
            pair (str): Forex pair

        Returns:
            dict: Multi-timeframe analysis
        """
        results = {}

        for timeframe in self.timeframes:
            results[timeframe] = self.scan_pair(pair, timeframe)

        return {
            'pair': pair,
            'timestamp': datetime.now().isoformat(),
            'timeframes': results
        }

    def get_active_signals(self, timeframe='H4'):
        """
        Get all active trading signals

        Args:
            timeframe (str): Timeframe to scan

        Returns:
            list: Active trading signals
        """
        all_results = self.scan_all_pairs(timeframe)

        active_signals = []

        for result in all_results:
            if 'error' in result:
                continue

            if result.get('signals'):
                for signal in result['signals']:
                    if signal['type'] in ['BUY', 'SELL']:
                        active_signals.append({
                            'pair': result['pair'],
                            'timeframe': timeframe,
                            **signal
                        })

        # Sort by confidence and risk/reward
        active_signals.sort(
            key=lambda x: (
                {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}.get(x.get('confidence', 'LOW'), 0),
                x.get('risk_reward', 0)
            ),
            reverse=True
        )

        return active_signals
