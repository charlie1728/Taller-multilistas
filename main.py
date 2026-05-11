# main.py

from flask import Flask, render_template
# Importamos las funciones que creamos
from data_loader import cargar_datos_multilista, generar_marcadores 

app = Flask(__name__)

@app.route('/')
def root():
    # 1. Cargar los datos del CSV en la MultiLista
    multi_lista_divipola = cargar_datos_multilista()
    
    # 2. Generar la lista de marcadores a partir de la MultiLista
    markers = generar_marcadores(multi_lista_divipola)
    
    # En caso de no encontrar marcadores, puedes centrar el mapa en Colombia
    if not markers:
         markers = [{
             'lat': 4.5709, 
             'lon': -74.2973, 
             'popup': 'No se cargaron marcadores. Mapa centrado en Colombia.'
         }]
         
    # Puedes usar la MultiLista para imprimir algo en la consola si quieres verificar la carga
    # print("Resumen de la carga:")
    # multi_lista_divipola.mostrar() 

    # 3. Pasar la lista de marcadores a la plantilla
    return render_template('index.html', markers=markers)

if __name__ == '__main__':
    # Usamos host="0.0.0.0" para ser accesible desde cualquier IP (aunque localhost es suficiente para desarrollo local)
    app.run(host="localhost", port=8082, debug=True)