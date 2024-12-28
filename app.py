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

if __name__ == '__main__':
    app.run(debug=True)
