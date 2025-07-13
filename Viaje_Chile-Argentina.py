import requests

API_KEY = "7880631f-7f73-4bd5-86bd-30d0be0c59d3"

def geocodificar(ciudad, pais):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "key": API_KEY,
        "q": f"{ciudad}, {pais}",
        "locale": "es",
        "limit": 1
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print("Error", r.json())
        return None
    datos = r.json()
    if not datos.get("hits"):
        print(f"No se pudo encontrar la ciudad: {ciudad}")
        return None
    punto = datos["hits"][0]["point"]
    return punto["lat"], punto["lng"]

def obtener_datos_viaje(origen_coords, destino_coords, transporte):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "key": API_KEY,
        "vehicle": transporte,
        "locale": "es",
        "instructions": "true",
        "point": [f"{origen_coords[0]},{origen_coords[1]}", f"{destino_coords[0]},{destino_coords[1]}"]
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error:", response.json())
        return None

    datos = response.json()
    if "paths" not in datos or not datos["paths"]:
        print("No se encontró ruta")
        return None

    path = datos["paths"][0]
    distancia_km = path["distance"] / 1000
    distancia_millas = distancia_km * 0.621371
    duracion_horas = path["time"] / 3600000  # ms -> horas
    narrativa = path["instructions"]

    return distancia_km, distancia_millas, duracion_horas, narrativa

def mostrar_narrativa(narrativa):
    print("--- Instrucciones ---")
    for paso in narrativa:
        print(f"- {paso['text']} ({paso['distance']:.1f} m)")

def main():
    print("=== Calculador de Viajes Chile - Argentina  ===")
    print("Opciones de transporte: auto, bicicleta, pie")
    transporte_map = {
        "auto": "car",
        "bici": "bike",
        "pie": "foot"
    }

    while True:
        origen = input("Ciudad de Origen (en Chile) (s para salir): ")
        if origen.lower() == 's':
            break
        destino = input("Ciudad de Destino (en Argentina) (s para salir): ")
        if destino.lower() == 's':
            break

        transporte = input("Elige medio de transporte (auto/bici/pie) (s para salir): ")
        if transporte.lower() == 's':
            break
        if transporte.lower() not in transporte_map:
            print("Medio de transporte no válido (usa auto, bicicleta o pie).")
            continue

        transporte = transporte_map[transporte.lower()]

        origen_coords = geocodificar(origen, "Chile")
        if origen_coords is None:
            continue

        destino_coords = geocodificar(destino, "Argentina")
        if destino_coords is None:
            continue

        resultado = obtener_datos_viaje(origen_coords, destino_coords, transporte)
        if resultado is None:
            continue

        distancia_km, distancia_millas, duracion_horas, narrativa = resultado
        print(f"--- Detalles del Viaje ---")
        print(f"Desde: {origen.title()} ")
        print(f"Hasta: {destino.title()} ")
        print(f"Distancia: {distancia_km:.1f} km | {distancia_millas:.1f} millas")
        print(f"Duración aproximada en {transporte}: {duracion_horas:.1f} horas")

        mostrar_narrativa(narrativa)
        print()

if __name__ == "__main__":
    main()