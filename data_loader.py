import csv
import os
from Node import MultiLista 

# Nombre del archivo CSV
CSV_FILENAME = "DIVIPOLA-_C_digos_municipios_20250505.csv"

# Definir la ruta completa al archivo CSV
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), CSV_FILENAME)

def cargar_datos_multilista():
    """
    Carga los datos del CSV en una MultiLista.
    Incluye depuración y manejo de errores de formato/encabezado,
    corrigiendo el mapeo de columnas del CSV.
    """
    multi_lista = MultiLista()
    
    # === IMPRESIONES DE DEPURACIÓN ===
    print(f"\n--- INICIANDO CARGA CSV ---")
    print(f"Ruta esperada del CSV: {CSV_FILE_PATH}")
    
    if not os.path.exists(CSV_FILE_PATH):
        print(f"ERROR: EL ARCHIVO NO EXISTE EN LA RUTA: {CSV_FILE_PATH}")
        print("--- CARGA CSV TERMINADA CON FALLO ---")
        return multi_lista
    
    print(f"VERIFICACIÓN: Archivo encontrado exitosamente.")
    # =================================
    
    try:
        # Abrimos con 'utf-8-sig' para manejar el Byte Order Mark (BOM)
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8-sig') as file: 
            reader = csv.DictReader(file)
            
            # Lista de campos esperados, ajustada a los nombres exactos leídos del CSV
            expected_fields = ['Código', 'Nombre Departamento', 'Código Municipio', 'Nombre Municipio', 'Tipo: Municipio / Isla / Área no municipalizada', 'longitud', 'Latitud']
            
            # Verificación de encabezados
            if not all(field in reader.fieldnames for field in expected_fields):
                 print(f"¡ERROR DE LECTURA! Los encabezados no coinciden.")
                 print(f"Encabezados encontrados: {reader.fieldnames}")
                 print("--- CARGA CSV TERMINADA CON FALLO ---")
                 return multi_lista
            
            print(f"Encabezados del CSV verificados correctamente.")
            
            row_count = 0
            for i, row in enumerate(reader):
                
                # Omitir filas si faltan las coordenadas (evita el error 'NoneType' al llamar .replace)
                if row.get('Tipo: Municipio / Isla / Área no municipalizada') is None or row.get('longitud') is None:
                    continue 

                row_count += 1
                
                # Depuración de la primera fila
                if i == 0:
                    print(f"Leyendo primera fila (mapeo): {row}")

                # 1. Obtener datos del Departamento (Nodo principal)
                codigo_departamento = row['Código'] 
                nombre_departamento = row['Departamento']
                
                # 2. Insertar el Departamento si no existe
                multi_lista.insertar(nombre_departamento, codigo_departamento)
                
                # 3. Obtener datos del Municipio (Elemento de sublista)
                municipio_data = {
                    # Mapeo corregido basado en la estructura real del CSV:
                    
                    # El código del municipio estaba en 'Nombre Departamento'
                    'Código Municipio': row['Nombre Departamento'], 
                    # El nombre del municipio estaba en 'Código Municipio'
                    'Nombre Municipio': row['Código Municipio'], 
                    
                    # CORRECCIÓN CRÍTICA DE COORDENADAS:
                    # El campo 'Tipo: Municipio / Isla / Área no municipalizada' tiene la Longitud
                    'lon': float(row['Tipo: Municipio / Isla / Área no municipalizada'].replace(',', '.').strip('"')),
                    # El campo 'longitud' tiene la Latitud
                    'lat': float(row['longitud'].replace(',', '.').strip('"')),
                    
                    # El tipo ('Municipio' o 'Área no municipalizada') estaba en 'Nombre Municipio'
                    'Tipo': row['Nombre Municipio'] 
                }
                
                # 4. Agregar el Municipio a la sublista de su Departamento
                multi_lista.agregar_sublista(codigo_departamento, municipio_data)
                
            print(f"Filas procesadas con éxito: {row_count}")
            print("--- CARGA CSV TERMINADA CON ÉXITO ---")

    except KeyError as e:
        print(f"ERROR: No se encontró la columna {e}. Revisa la ortografía de los encabezados del CSV.")
        print("--- CARGA CSV TERMINADA CON FALLO ---")
    except Exception as e:
        print(f"ERROR DURANTE EL PROCESAMIENTO DEL CSV: {e}")
        print("--- CARGA CSV TERMINADA CON FALLO ---")
        
    return multi_lista

def generar_marcadores(multi_lista):
    """
    Recorre la MultiLista y genera el formato de marcadores para Leaflet.
    """
    markers = []
    actual = multi_lista.cabeza
    
    while actual:
        for municipio in actual.sublista:
            try:
                # Crear el texto del popup
                popup_text = f"**{municipio['Nombre Municipio']}** ({municipio['Tipo']})<br>Departamento: {actual.name}"
                
                # Crear el marcador
                marker = {
                    'lat': municipio['lat'],
                    'lon': municipio['lon'],
                    'popup': popup_text
                }
                markers.append(marker)
            except Exception as e:
                print(f"Advertencia: No se pudo generar el marcador para {municipio.get('Nombre Municipio')}: {e}")
                
        actual = actual.next
        
    return markers
