# archivo: app.py
from flask import Flask, request, jsonify, redirect
import json
import string
import random
import os

app = Flask(__name__)
DATA_FILE = "urls.json"

# Cargar datos existentes
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        url_map = json.load(f)
else:
    url_map = {}

# Función para generar un código corto
def generar_codigo(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if code not in url_map:
            return code

# Endpoint para acortar URL
@app.route("/api/shorten", methods=["POST"])
def shorten():
    data = request.json
    long_url = data.get("url")
    if not long_url:
        return jsonify({"error": "Se requiere 'url'"}), 400

    code = generar_codigo()
    url_map[code] = long_url

    # Guardar en el archivo
    with open(DATA_FILE, "w") as f:
        json.dump(url_map, f)

    short_url = request.host_url + code
    return jsonify({"short_url": short_url})

# Endpoint para redirigir URLs cortas
@app.route("/<code>")
def redirect_url(code):
    long_url = url_map.get(code)
    if long_url:
        return redirect(long_url)
    else:
        return jsonify({"error": "URL no encontrada"}), 404

# Ejecutar API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
