from flask import Flask, render_template, jsonify
import os
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)

# Fonction pour charger les données
def load_data():
    try:
        with open('data/whisky_prices.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"whiskies": [], "last_updated": ""}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/whisky/<whisky_name>')
def whisky_detail(whisky_name):
    return render_template('whisky_detail.html', whisky_name=whisky_name)

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/api/whiskies')
def get_whiskies():
    data = load_data()
    return jsonify(data)

@app.route('/api/whisky/<whisky_name>')
def get_whisky(whisky_name):
    data = load_data()
    for whisky in data["whiskies"]:
        if whisky["name"].lower() == whisky_name.lower():
            return jsonify(whisky)
    return jsonify({"error": "Whisky not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
