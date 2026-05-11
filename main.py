# main.py

from flask import Flask, render_template, jsonify
# Importamos las funciones que creamos
from data_loader import cargar_datos_multilista, generar_marcadores

app = Flask(__name__)

# Cache global para evitar recargar el CSV múltiples veces
_multilista_cache = None
_marcadores_cache = None

def get_multilista():
    """Obtiene la multilista, usando caché para mejor rendimiento"""
    global _multilista_cache
    if _multilista_cache is None:
        _multilista_cache = cargar_datos_multilista()
    return _multilista_cache

def get_marcadores():
    """Obtiene los marcadores, usando caché"""
    global _marcadores_cache
    if _marcadores_cache is None:
        _marcadores_cache = generar_marcadores(get_multilista())
    return _marcadores_cache

@app.route('/')
def root():
    """Ruta principal: visualiza el mapa interactivo"""
    markers = get_marcadores()

    # En caso de no encontrar marcadores, puedes centrar el mapa en Colombia
    if not markers:
         markers = [{
             'lat': 4.5709,
             'lon': -74.2973,
             'popup': 'No se cargaron marcadores. Mapa centrado en Colombia.'
         }]

    # Pasar la lista de marcadores a la plantilla
    return render_template('index.html', markers=markers)

@app.route('/api/multilista')
def api_multilista():
    """Endpoint API: expone la multilista completa en formato JSON"""
    multilista = get_multilista()
    return jsonify(multilista.a_json())

@app.route('/api/marcadores')
def api_marcadores():
    """Endpoint API: expone los marcadores en formato JSON"""
    marcadores = get_marcadores()
    return jsonify({
        "total": len(marcadores),
        "marcadores": marcadores
    })

@app.route('/api/info')
def api_info():
    """Endpoint API: información general sobre la API"""
    return jsonify({
        "nombre": "API DIVIPOLA",
        "descripcion": "Multilista Jerárquica de la División Político-Administrativa de Colombia",
        "endpoints": {
            "/": "Visualización interactiva del mapa",
            "/api/multilista": "Obtiene la estructura completa de la multilista (País → Departamentos → Municipios)",
            "/api/marcadores": "Obtiene la lista de marcadores para el mapa",
            "/api/info": "Esta información"
        }
    })

if __name__ == '__main__':
    # Usamos host="0.0.0.0" para ser accesible desde cualquier IP (aunque localhost es suficiente para desarrollo local)
    app.run(host="localhost", port=8082, debug=True)
