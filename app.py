# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import MetaTrader5 as mt5
import pandas as pd
from config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_PATH

app = Flask(__name__)

# Initialize MT5
def init_mt5():
    if not mt5.initialize(MT5_PATH, login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        return {"success": False, "error": mt5.last_error()}
    return {"success": True}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account_info')
def account_info():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    account_info = mt5.account_info()._asdict()
    return jsonify(account_info), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/symbols')
def symbols():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    symbols = mt5.symbols_get()
    symbols_data = [symbol._asdict() for symbol in symbols]
    return jsonify(symbols_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/market_data/<symbol>')
def market_data(symbol):
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 10)
    if rates is None:
        return jsonify({"error": mt5.last_error()})
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return jsonify(df.to_dict(orient='records')), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/orders')
def orders():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    orders = mt5.orders_get()
    orders_data = [order._asdict() for order in orders]
    return jsonify(orders_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/positions')
def positions():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    positions = mt5.positions_get()
    positions_data = [position._asdict() for position in positions]
    return jsonify(positions_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/orders_history')
def orders_history():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    orders_history = mt5.history_orders_get()
    orders_history_data = [order._asdict() for order in orders_history]
    return jsonify(orders_history_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/positions_history')
def positions_history():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    positions_history = mt5.history_positions_get()
    positions_history_data = [position._asdict() for position in positions_history]
    return jsonify(positions_history_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/news')
def news():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    news_data = mt5.news_get()
    return jsonify(news_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/economic_calendar')
def economic_calendar():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    calendar_data = mt5.calendar_economic_get()
    return jsonify(calendar_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/trade_operations')
def trade_operations():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    trade_operations = mt5.trades_get()
    trade_operations_data = [trade._asdict() for trade in trade_operations]
    return jsonify(trade_operations_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/accounts')
def accounts():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    accounts = mt5.accounts_get()
    accounts_data = [account._asdict() for account in accounts]
    return jsonify(accounts_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/account_history')
def account_history():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    account_history = mt5.history_orders_get()
    account_history_data = [entry._asdict() for entry in account_history]
    return jsonify(account_history_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/calendar_events')
def calendar_events():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    calendar_events = mt5.calendar_events_get()
    events_data = [event._asdict() for event in calendar_events]
    return jsonify(events_data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/trade_request', methods=['POST'])
def trade_request():
    result = init_mt5()
    if not result["success"]:
        return jsonify({"error": result["error"]})
    request_data = request.json
    action = request_data.get('action')
    symbol = request_data.get('symbol')
    volume = request_data.get('volume')
    price = request_data.get('price')

    if action not in ['buy', 'sell']:
        return jsonify({"error": "Invalid trade action. Use 'buy' or 'sell'."})

    if action == 'buy':
        order = mt5.order_buy(symbol, volume, price)
    else:  # action == 'sell'
        order = mt5.order_sell(symbol, volume, price)

    if order is None:
        return jsonify({"error": mt5.last_error()})
    return jsonify(order._asdict()), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True)
