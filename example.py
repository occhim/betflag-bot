"""
Example usage of Forex Trading Analysis App
Demonstrates all main features
"""
from src.scanner import ForexScanner
from src.oanda_client import OandaClient
from src.pattern_detector import PatternDetector
from src.support_resistance import SupportResistance
from src.backtester import Backtester
from config import Config


def example_scanner():
    """Example: Multi-pair scanner"""
    print("=" * 60)
    print("EXAMPLE 1: Multi-Pair Scanner")
    print("=" * 60)

    scanner = ForexScanner()

    # Scan single pair
    print("\n1. Scanning EUR/USD on H4 timeframe...")
    result = scanner.scan_pair('EUR_USD', timeframe='H4')

    if 'error' not in result:
        print(f"\nPair: {result['pair']}")
        print(f"Current Price: {result['current_price']}")
        print(f"At Key Level: {result['at_key_level']}")

        if result['recent_patterns']:
            print(f"\nRecent Patterns:")
            for pattern_info in result['recent_patterns']:
                print(f"  - {pattern_info['time']}: {', '.join(pattern_info['patterns'])}")

        if result['signals']:
            print(f"\nTrading Signals:")
            for signal in result['signals']:
                print(f"  - {signal['type']}: {signal['reason']}")
                if signal['type'] in ['BUY', 'SELL']:
                    print(f"    Entry: {signal['entry']}")
                    print(f"    Stop: {signal['stop_loss']}")
                    print(f"    Target: {signal['take_profit']}")
                    print(f"    R/R: 1:{signal['risk_reward']}")
    else:
        print(f"Error: {result['error']}")

    # Get all active signals
    print("\n2. Getting active signals across all pairs...")
    signals = scanner.get_active_signals(timeframe='H4')

    print(f"\nFound {len(signals)} active signals:")
    for signal in signals[:5]:  # Show top 5
        print(f"  - {signal['pair']}: {signal['type']} ({signal['confidence']})")


def example_pattern_detection():
    """Example: Pattern detection"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Pattern Detection")
    print("=" * 60)

    client = OandaClient()
    df = client.get_candles('GBP_USD', granularity='H4', count=200)

    if df is not None:
        detector = PatternDetector(df)
        detector.detect_all_patterns()

        print(f"\nAnalyzed {len(df)} candles for GBP/USD")

        # Count patterns
        pin_bars = df['pin_bar'].sum() if 'pin_bar' in df.columns else 0
        engulfing = df['engulfing'].sum() if 'engulfing' in df.columns else 0
        inside_bars = df['inside_bar'].sum() if 'inside_bar' in df.columns else 0
        dojis = df['doji'].sum() if 'doji' in df.columns else 0

        print(f"\nPattern Count:")
        print(f"  - Pin Bars: {pin_bars}")
        print(f"  - Engulfing: {engulfing}")
        print(f"  - Inside Bars: {inside_bars}")
        print(f"  - Dojis: {dojis}")

        # Recent patterns
        recent = detector.get_recent_patterns(last_n=5)
        if recent:
            print(f"\nLast 5 patterns:")
            for p in recent:
                print(f"  - {p['time']}: {', '.join(p['patterns'])}")


def example_support_resistance():
    """Example: Support/Resistance detection"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Support/Resistance Detection")
    print("=" * 60)

    client = OandaClient()
    df = client.get_candles('EUR_USD', granularity='H4', count=200)

    if df is not None:
        sr = SupportResistance(df)
        levels = sr.detect_support_resistance()

        print(f"\nSupport Levels (top 5):")
        for i, level in enumerate(levels['support'][:5], 1):
            print(f"  {i}. Price: {level['price']:.5f}, Strength: {level['strength']}")

        print(f"\nResistance Levels (top 5):")
        for i, level in enumerate(levels['resistance'][:5], 1):
            print(f"  {i}. Price: {level['price']:.5f}, Strength: {level['strength']}")

        # Current price and nearest levels
        current_price = df['close'].iloc[-1]
        nearest = sr.get_nearest_levels(current_price)

        print(f"\nCurrent Price: {current_price:.5f}")
        print(f"\nNearest Support:")
        for s in nearest['support'][:3]:
            distance_pips = (current_price - s['price']) / 0.0001
            print(f"  - {s['price']:.5f} ({distance_pips:.1f} pips below)")

        print(f"\nNearest Resistance:")
        for r in nearest['resistance'][:3]:
            distance_pips = (r['price'] - current_price) / 0.0001
            print(f"  - {r['price']:.5f} ({distance_pips:.1f} pips above)")

        # Risk/Reward calculation
        print(f"\n--- Risk/Reward for Long Trade ---")
        rr = sr.calculate_risk_reward(current_price, 'long')
        print(f"Entry: {rr['entry']:.5f}")
        print(f"Stop Loss: {rr['stop_loss']:.5f} ({rr['risk_pips']:.1f} pips)")
        print(f"Take Profit: {rr['take_profit']:.5f} ({rr['reward_pips']:.1f} pips)")
        print(f"Risk/Reward Ratio: 1:{rr['risk_reward_ratio']}")


def example_backtesting():
    """Example: Backtesting patterns"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Backtesting")
    print("=" * 60)

    print("\nFetching historical data...")
    client = OandaClient()
    df = client.get_candles('EUR_USD', granularity='H4', count=2000)

    if df is not None:
        print(f"Testing on {len(df)} candles (EUR/USD H4)")

        backtester = Backtester(initial_balance=10000, risk_per_trade=1.0)

        # Test Pin Bar pattern
        print("\nBacktesting Pin Bar pattern...")
        results = backtester.backtest_pattern(
            df,
            pattern_type='pin_bar',
            direction='both',
            min_rr=1.5
        )

        print(f"\n--- Pin Bar Backtest Results ---")
        print(f"Total Trades: {results['total_trades']}")
        print(f"Winning Trades: {results['winning_trades']}")
        print(f"Losing Trades: {results['losing_trades']}")
        print(f"Win Rate: {results['win_rate']}%")
        print(f"Total P&L: ${results['total_pnl']:.2f}")
        print(f"Total Return: {results['total_return']}%")
        print(f"Final Balance: ${results['final_balance']:.2f}")
        print(f"Max Drawdown: {results['max_drawdown']}%")
        print(f"Profit Factor: {results['profit_factor']}")
        print(f"Avg Win: ${results['avg_win']:.2f} ({results['avg_win_pips']:.1f} pips)")
        print(f"Avg Loss: ${results['avg_loss']:.2f} ({results['avg_loss_pips']:.1f} pips)")
        print(f"Avg Bars Held: {results['avg_bars_held']:.1f}")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("FOREX TRADING ANALYSIS APP - EXAMPLES")
    print("=" * 60)

    # Check API configuration
    if not Config.OANDA_API_KEY:
        print("\n⚠️  WARNING: OANDA API key not configured!")
        print("Please set OANDA_API_KEY in your .env file")
        print("\nYou can still run the examples, but they will use demo/cached data")
        print("=" * 60)

    try:
        # Run examples
        example_scanner()
        example_pattern_detection()
        example_support_resistance()

        # Backtesting takes longer, ask first
        print("\n" + "=" * 60)
        response = input("\nRun backtesting example? (takes ~30 seconds) [y/N]: ")
        if response.lower() == 'y':
            example_backtesting()

        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Configure your .env file with OANDA API credentials")
        print("2. Run the web app: python app.py")
        print("3. Open http://localhost:5000 in your browser")
        print("\nFor more info, see README_FOREX.md")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Installed all dependencies (pip install -r requirements.txt)")
        print("2. Configured OANDA API credentials in .env")
        print("3. TA-Lib installed (see README_FOREX.md)")


if __name__ == '__main__':
    main()
