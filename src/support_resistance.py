"""
Support and Resistance Level Detection
"""
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema


class SupportResistance:
    """Detect support and resistance levels using price action"""

    def __init__(self, df, lookback=100, tolerance=0.0005):
        """
        Initialize S/R detector

        Args:
            df (pd.DataFrame): OHLC data
            lookback (int): Number of candles to look back
            tolerance (float): Price tolerance for level clustering (in decimal, e.g., 0.0005 = 5 pips)
        """
        self.df = df.copy()
        self.lookback = lookback
        self.tolerance = tolerance
        self.support_levels = []
        self.resistance_levels = []

    def find_pivot_points(self, order=5):
        """
        Find pivot highs and lows using local extrema

        Args:
            order (int): How many points on each side to use for comparison

        Returns:
            tuple: (pivot_highs, pivot_lows)
        """
        # Find local maxima (resistance)
        highs_idx = argrelextrema(
            self.df['high'].values,
            np.greater,
            order=order
        )[0]

        # Find local minima (support)
        lows_idx = argrelextrema(
            self.df['low'].values,
            np.less,
            order=order
        )[0]

        pivot_highs = self.df.iloc[highs_idx][['high']].copy()
        pivot_highs['type'] = 'resistance'

        pivot_lows = self.df.iloc[lows_idx][['low']].copy()
        pivot_lows['type'] = 'support'

        return pivot_highs, pivot_lows

    def cluster_levels(self, levels, price_column):
        """
        Cluster nearby price levels into zones

        Args:
            levels (pd.DataFrame): Pivot points
            price_column (str): Column name ('high' or 'low')

        Returns:
            list: Clustered levels with strength
        """
        if levels.empty:
            return []

        prices = levels[price_column].values
        clusters = []

        for price in prices:
            # Find if price belongs to existing cluster
            added = False
            for cluster in clusters:
                if abs(price - cluster['price']) <= cluster['price'] * self.tolerance:
                    # Add to existing cluster
                    cluster['prices'].append(price)
                    cluster['price'] = np.mean(cluster['prices'])
                    cluster['strength'] += 1
                    added = True
                    break

            if not added:
                # Create new cluster
                clusters.append({
                    'price': price,
                    'prices': [price],
                    'strength': 1
                })

        # Sort by strength
        clusters.sort(key=lambda x: x['strength'], reverse=True)

        return clusters

    def detect_support_resistance(self, order=5, min_strength=2):
        """
        Detect support and resistance levels

        Args:
            order (int): Order for pivot point detection
            min_strength (int): Minimum touches for a valid level

        Returns:
            dict: Support and resistance levels
        """
        # Get recent data
        recent_df = self.df.tail(self.lookback)
        self.df = recent_df

        # Find pivot points
        pivot_highs, pivot_lows = self.find_pivot_points(order=order)

        # Cluster levels
        resistance_clusters = self.cluster_levels(pivot_highs, 'high')
        support_clusters = self.cluster_levels(pivot_lows, 'low')

        # Filter by minimum strength
        self.resistance_levels = [
            {
                'price': c['price'],
                'strength': c['strength'],
                'type': 'resistance'
            }
            for c in resistance_clusters if c['strength'] >= min_strength
        ]

        self.support_levels = [
            {
                'price': c['price'],
                'strength': c['strength'],
                'type': 'support'
            }
            for c in support_clusters if c['strength'] >= min_strength
        ]

        return {
            'support': self.support_levels,
            'resistance': self.resistance_levels
        }

    def get_nearest_levels(self, current_price, max_levels=3):
        """
        Get nearest support and resistance levels to current price

        Args:
            current_price (float): Current market price
            max_levels (int): Maximum levels to return for each type

        Returns:
            dict: Nearest support and resistance levels
        """
        # Find nearest support (below current price)
        supports_below = [
            s for s in self.support_levels
            if s['price'] < current_price
        ]
        supports_below.sort(key=lambda x: current_price - x['price'])
        nearest_support = supports_below[:max_levels]

        # Find nearest resistance (above current price)
        resistances_above = [
            r for r in self.resistance_levels
            if r['price'] > current_price
        ]
        resistances_above.sort(key=lambda x: x['price'] - current_price)
        nearest_resistance = resistances_above[:max_levels]

        return {
            'support': nearest_support,
            'resistance': nearest_resistance,
            'current_price': current_price
        }

    def is_at_level(self, price, level_type='both', tolerance_multiplier=1.5):
        """
        Check if price is at a support or resistance level

        Args:
            price (float): Price to check
            level_type (str): 'support', 'resistance', or 'both'
            tolerance_multiplier (float): Multiplier for tolerance

        Returns:
            dict: Information about nearby levels
        """
        tolerance = price * self.tolerance * tolerance_multiplier
        nearby = {
            'at_support': False,
            'at_resistance': False,
            'support_level': None,
            'resistance_level': None
        }

        if level_type in ['support', 'both']:
            for support in self.support_levels:
                if abs(price - support['price']) <= tolerance:
                    nearby['at_support'] = True
                    nearby['support_level'] = support
                    break

        if level_type in ['resistance', 'both']:
            for resistance in self.resistance_levels:
                if abs(price - resistance['price']) <= tolerance:
                    nearby['at_resistance'] = True
                    nearby['resistance_level'] = resistance
                    break

        return nearby

    def calculate_risk_reward(self, entry_price, direction, stop_loss_pips=None, take_profit_pips=None):
        """
        Calculate risk/reward based on nearest levels

        Args:
            entry_price (float): Entry price
            direction (str): 'long' or 'short'
            stop_loss_pips (float): Optional manual stop loss in pips
            take_profit_pips (float): Optional manual take profit in pips

        Returns:
            dict: Risk/reward calculation
        """
        nearest = self.get_nearest_levels(entry_price)

        if direction == 'long':
            # For long: stop at support, target at resistance
            if stop_loss_pips:
                stop_loss = entry_price - (stop_loss_pips * 0.0001)
            else:
                stop_loss = nearest['support'][0]['price'] if nearest['support'] else entry_price * 0.99

            if take_profit_pips:
                take_profit = entry_price + (take_profit_pips * 0.0001)
            else:
                take_profit = nearest['resistance'][0]['price'] if nearest['resistance'] else entry_price * 1.01

        else:  # short
            # For short: stop at resistance, target at support
            if stop_loss_pips:
                stop_loss = entry_price + (stop_loss_pips * 0.0001)
            else:
                stop_loss = nearest['resistance'][0]['price'] if nearest['resistance'] else entry_price * 1.01

            if take_profit_pips:
                take_profit = entry_price - (take_profit_pips * 0.0001)
            else:
                take_profit = nearest['support'][0]['price'] if nearest['support'] else entry_price * 0.99

        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        risk_reward_ratio = reward / risk if risk > 0 else 0

        return {
            'entry': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk': risk,
            'reward': reward,
            'risk_reward_ratio': round(risk_reward_ratio, 2),
            'risk_pips': round(risk / 0.0001, 1),
            'reward_pips': round(reward / 0.0001, 1)
        }
