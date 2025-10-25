"""
Backtesting system for pattern-based trading strategies
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.pattern_detector import PatternDetector
from src.support_resistance import SupportResistance
from src.oanda_client import OandaClient


class Backtester:
    """Backtest price action patterns"""

    def __init__(self, initial_balance=10000, risk_per_trade=1.0):
        """
        Initialize backtester

        Args:
            initial_balance (float): Starting account balance
            risk_per_trade (float): Risk percentage per trade
        """
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.trades = []
        self.equity_curve = []

    def backtest_pattern(self, df, pattern_type, direction='both', min_rr=1.5):
        """
        Backtest a specific candlestick pattern

        Args:
            df (pd.DataFrame): OHLC data
            pattern_type (str): Pattern to test ('pin_bar', 'engulfing', etc.)
            direction (str): 'long', 'short', or 'both'
            min_rr (float): Minimum risk/reward ratio

        Returns:
            dict: Backtest results
        """
        # Detect patterns
        pattern_detector = PatternDetector(df)
        pattern_detector.detect_all_patterns()

        # Detect S/R levels for each trade
        for i in range(len(df)):
            if i < 50:  # Need enough history
                continue

            # Check if pattern exists at this candle
            has_pattern = False
            trade_direction = None

            if pattern_type == 'pin_bar' and df.iloc[i].get('pin_bar', False):
                has_pattern = True
                pin_type = df.iloc[i].get('pin_bar_type')
                if pin_type == 'bullish_hammer':
                    trade_direction = 'long'
                elif pin_type == 'bearish_shooting_star':
                    trade_direction = 'short'

            elif pattern_type == 'engulfing' and df.iloc[i].get('engulfing', False):
                has_pattern = True
                eng_type = df.iloc[i].get('engulfing_type')
                if eng_type == 'bullish_engulfing':
                    trade_direction = 'long'
                elif eng_type == 'bearish_engulfing':
                    trade_direction = 'short'

            elif pattern_type == 'morning_evening_star' and df.iloc[i].get('star', False):
                has_pattern = True
                star_type = df.iloc[i].get('star_type')
                if star_type == 'morning_star':
                    trade_direction = 'long'
                elif star_type == 'evening_star':
                    trade_direction = 'short'

            if not has_pattern or not trade_direction:
                continue

            # Skip if direction filter doesn't match
            if direction != 'both' and direction != trade_direction:
                continue

            # Calculate S/R levels for this point in time
            historical_df = df.iloc[:i+1]
            sr_detector = SupportResistance(historical_df.tail(100))
            sr_detector.detect_support_resistance()

            # Entry on next candle open
            if i + 1 >= len(df):
                break

            entry_price = df.iloc[i + 1]['open']

            # Calculate stop loss and take profit
            rr = sr_detector.calculate_risk_reward(entry_price, trade_direction)

            if rr['risk_reward_ratio'] < min_rr:
                continue

            # Simulate trade
            trade_result = self._simulate_trade(
                df.iloc[i+1:],
                entry_price,
                rr['stop_loss'],
                rr['take_profit'],
                trade_direction
            )

            if trade_result:
                trade_result['entry_time'] = df.index[i + 1]
                trade_result['pattern'] = pattern_type
                trade_result['direction'] = trade_direction
                self.trades.append(trade_result)

        return self._calculate_statistics()

    def _simulate_trade(self, future_df, entry, stop_loss, take_profit, direction):
        """
        Simulate a single trade

        Args:
            future_df (pd.DataFrame): Future price data
            entry (float): Entry price
            stop_loss (float): Stop loss price
            take_profit (float): Take profit price
            direction (str): 'long' or 'short'

        Returns:
            dict: Trade result
        """
        risk_amount = self.balance * (self.risk_per_trade / 100)

        for i, (idx, candle) in enumerate(future_df.iterrows()):
            if direction == 'long':
                # Check stop loss
                if candle['low'] <= stop_loss:
                    loss = risk_amount
                    self.balance -= loss
                    return {
                        'exit_time': idx,
                        'exit_price': stop_loss,
                        'result': 'loss',
                        'pnl': -loss,
                        'pnl_pips': (stop_loss - entry) / 0.0001,
                        'bars_held': i + 1
                    }

                # Check take profit
                if candle['high'] >= take_profit:
                    rr_ratio = abs(take_profit - entry) / abs(entry - stop_loss)
                    profit = risk_amount * rr_ratio
                    self.balance += profit
                    return {
                        'exit_time': idx,
                        'exit_price': take_profit,
                        'result': 'win',
                        'pnl': profit,
                        'pnl_pips': (take_profit - entry) / 0.0001,
                        'bars_held': i + 1
                    }

            else:  # short
                # Check stop loss
                if candle['high'] >= stop_loss:
                    loss = risk_amount
                    self.balance -= loss
                    return {
                        'exit_time': idx,
                        'exit_price': stop_loss,
                        'result': 'loss',
                        'pnl': -loss,
                        'pnl_pips': (entry - stop_loss) / 0.0001,
                        'bars_held': i + 1
                    }

                # Check take profit
                if candle['low'] <= take_profit:
                    rr_ratio = abs(entry - take_profit) / abs(stop_loss - entry)
                    profit = risk_amount * rr_ratio
                    self.balance += profit
                    return {
                        'exit_time': idx,
                        'exit_price': take_profit,
                        'result': 'win',
                        'pnl': profit,
                        'pnl_pips': (entry - take_profit) / 0.0001,
                        'bars_held': i + 1
                    }

            # Max 50 bars
            if i >= 50:
                # Close at market
                exit_price = candle['close']
                if direction == 'long':
                    pnl_pips = (exit_price - entry) / 0.0001
                else:
                    pnl_pips = (entry - exit_price) / 0.0001

                pnl = (pnl_pips / abs((entry - stop_loss) / 0.0001)) * risk_amount

                self.balance += pnl
                return {
                    'exit_time': idx,
                    'exit_price': exit_price,
                    'result': 'timeout',
                    'pnl': pnl,
                    'pnl_pips': pnl_pips,
                    'bars_held': i + 1
                }

        return None

    def _calculate_statistics(self):
        """
        Calculate backtest statistics

        Returns:
            dict: Performance metrics
        """
        if not self.trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'total_return': 0,
                'max_drawdown': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'profit_factor': 0
            }

        df_trades = pd.DataFrame(self.trades)

        winning_trades = df_trades[df_trades['result'] == 'win']
        losing_trades = df_trades[df_trades['result'] == 'loss']

        total_pnl = df_trades['pnl'].sum()
        total_return = ((self.balance - self.initial_balance) / self.initial_balance) * 100

        # Calculate drawdown
        equity = self.initial_balance
        equity_curve = [equity]
        peak = equity

        for trade in self.trades:
            equity += trade['pnl']
            equity_curve.append(equity)
            if equity > peak:
                peak = equity

        drawdowns = [(peak - e) / peak * 100 for e in equity_curve]
        max_drawdown = max(drawdowns) if drawdowns else 0

        gross_profit = winning_trades['pnl'].sum() if not winning_trades.empty else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if not losing_trades.empty else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0

        return {
            'total_trades': len(self.trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': round((len(winning_trades) / len(self.trades)) * 100, 2),
            'total_pnl': round(total_pnl, 2),
            'total_return': round(total_return, 2),
            'final_balance': round(self.balance, 2),
            'max_drawdown': round(max_drawdown, 2),
            'avg_win': round(winning_trades['pnl'].mean(), 2) if not winning_trades.empty else 0,
            'avg_loss': round(losing_trades['pnl'].mean(), 2) if not losing_trades.empty else 0,
            'avg_win_pips': round(winning_trades['pnl_pips'].mean(), 1) if not winning_trades.empty else 0,
            'avg_loss_pips': round(losing_trades['pnl_pips'].mean(), 1) if not losing_trades.empty else 0,
            'profit_factor': round(profit_factor, 2),
            'avg_bars_held': round(df_trades['bars_held'].mean(), 1)
        }

    def run_comprehensive_backtest(self, pair, timeframe='H4', patterns=None):
        """
        Run backtest on multiple patterns

        Args:
            pair (str): Forex pair
            timeframe (str): Timeframe
            patterns (list): List of patterns to test

        Returns:
            dict: Results for all patterns
        """
        if patterns is None:
            patterns = ['pin_bar', 'engulfing', 'morning_evening_star']

        client = OandaClient()
        df = client.get_candles(pair, granularity=timeframe, count=5000)

        if df is None or df.empty:
            return {'error': 'Unable to fetch data'}

        results = {}

        for pattern in patterns:
            print(f"Backtesting {pattern} on {pair}...")

            # Reset for each pattern
            self.balance = self.initial_balance
            self.trades = []

            result = self.backtest_pattern(df, pattern)
            results[pattern] = result

        return {
            'pair': pair,
            'timeframe': timeframe,
            'initial_balance': self.initial_balance,
            'results': results
        }
