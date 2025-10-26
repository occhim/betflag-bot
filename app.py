"""
Forex Trading Analysis Web Application
Flask-based REST API for price action analysis
"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from src.scanner import ForexScanner
from src.oanda_client import OandaClient
from src.support_resistance import SupportResistance
from config import Config
import os

app = Flask(__name__)
CORS(app)

# Initialize scanner
scanner = ForexScanner()


@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html')


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'api_configured': bool(Config.OANDA_API_KEY)
    })


@app.route('/api/pairs')
def get_pairs():
    """Get list of available forex pairs"""
    return jsonify({
        'pairs': Config.DEFAULT_PAIRS,
        'timeframes': Config.TIMEFRAMES
    })


@app.route('/api/scan/<pair>')
def scan_pair(pair):
    """
    Scan single pair for patterns

    Args:
        pair (str): Forex pair (e.g., EUR_USD)
        timeframe (str): Optional timeframe query param

    Returns:
        JSON: Scan results
    """
    timeframe = request.args.get('timeframe', 'H4')

    try:
        result = scanner.scan_pair(pair, timeframe)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/all')
def scan_all():
    """
    Scan all pairs

    Returns:
        JSON: All scan results
    """
    timeframe = request.args.get('timeframe', 'H4')

    try:
        results = scanner.scan_all_pairs(timeframe)
        return jsonify({
            'timeframe': timeframe,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/multi-timeframe/<pair>')
def scan_multi_timeframe(pair):
    """
    Scan pair across multiple timeframes

    Args:
        pair (str): Forex pair

    Returns:
        JSON: Multi-timeframe analysis
    """
    try:
        result = scanner.scan_multi_timeframe(pair)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/signals')
def get_signals():
    """
    Get active trading signals

    Returns:
        JSON: Active signals
    """
    timeframe = request.args.get('timeframe', 'H4')

    try:
        signals = scanner.get_active_signals(timeframe)
        return jsonify({
            'timeframe': timeframe,
            'count': len(signals),
            'signals': signals
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/price/<pair>')
def get_price(pair):
    """
    Get current price for a pair

    Args:
        pair (str): Forex pair

    Returns:
        JSON: Current price data
    """
    try:
        client = OandaClient()
        price = client.get_current_price(pair)

        if price:
            return jsonify({
                'pair': pair,
                **price
            })
        else:
            return jsonify({'error': 'Price not available'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/risk-calculator', methods=['POST'])
def calculate_risk():
    """
    Calculate risk/reward for a trade

    POST JSON body:
    {
        "pair": "EUR_USD",
        "entry": 1.1000,
        "direction": "long",
        "stop_loss_pips": 20,
        "take_profit_pips": 40,
        "account_size": 10000,
        "risk_percent": 1
    }

    Returns:
        JSON: Risk/reward calculation
    """
    try:
        data = request.json

        pair = data.get('pair')
        entry = float(data.get('entry'))
        direction = data.get('direction', 'long')
        stop_loss_pips = data.get('stop_loss_pips')
        take_profit_pips = data.get('take_profit_pips')
        account_size = float(data.get('account_size', 10000))
        risk_percent = float(data.get('risk_percent', 1))

        # Get data for S/R levels
        client = OandaClient()
        df = client.get_candles(pair, granularity='H4', count=200)

        if df is None:
            return jsonify({'error': 'Unable to fetch data'}), 400

        sr_detector = SupportResistance(df)
        sr_detector.detect_support_resistance()

        # Calculate R/R
        rr = sr_detector.calculate_risk_reward(
            entry,
            direction,
            stop_loss_pips,
            take_profit_pips
        )

        # Calculate position size
        risk_amount = account_size * (risk_percent / 100)
        pip_value = 10 if 'JPY' in pair else 1  # Simplified
        position_size = risk_amount / (rr['risk_pips'] * pip_value)

        result = {
            **rr,
            'account_size': account_size,
            'risk_percent': risk_percent,
            'risk_amount': round(risk_amount, 2),
            'position_size_lots': round(position_size / 100000, 2),  # Standard lots
            'potential_profit': round(risk_amount * rr['risk_reward_ratio'], 2)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', Config.PORT))
    debug = Config.FLASK_DEBUG

    print(f"""
    ╔════════════════════════════════════════════════════╗
    ║   Forex Trading Analysis App                       ║
    ║   Price Action & Pattern Recognition System        ║
    ╚════════════════════════════════════════════════════╝

    Server running on: http://localhost:{port}

    API Endpoints:
    - GET  /api/health              - Health check
    - GET  /api/pairs               - Available pairs
    - GET  /api/scan/<pair>         - Scan single pair
    - GET  /api/scan/all            - Scan all pairs
    - GET  /api/scan/multi-timeframe/<pair> - Multi-TF analysis
    - GET  /api/signals             - Get active signals
    - GET  /api/price/<pair>        - Current price
    - POST /api/risk-calculator     - Calculate R/R

    Make sure to configure your .env file with OANDA credentials!
    """)

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
