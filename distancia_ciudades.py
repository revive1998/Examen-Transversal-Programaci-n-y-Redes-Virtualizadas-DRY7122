import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "951d48f9-464a-4ce9-a812-04313789f315"

def geocoding(location, key):
    while location == "":
        location = input("Ingresa nuevamente la ubicación: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        new_loc = name
        if state and country:
            new_loc += f", {state}, {country}"
        elif country:
            new_loc += f", {country}"

        print(f"URL Geocoding para {new_loc} (Tipo de ubicación: {value})\n{url}")
    else:
        lat, lng, new_loc = "null", "null", location
        if json_status != 200:
            print(f"Estado del Geocoding API: {json_status}\nMensaje de error: {json_data['message']}")
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car (auto), bike (bicicleta), foot (a pie)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    perfiles = ["car", "bike", "foot"]
    vehiculo = input("Elige el tipo de transporte: ").strip().lower()
    if vehiculo not in perfiles:
        print("Perfil no válido. Usando 'car' por defecto.")
        vehiculo = "car"

    loc1 = input("Ciudad de Origen (o escribe 's' para salir): ").strip()
    if loc1.lower() == "s":
        print("¡Hasta luego!")
        break
    origen = geocoding(loc1, key)

    loc2 = input("Ciudad de Destino (o escribe 's' para salir): ").strip()
    if loc2.lower() == "s":
        print("¡Hasta luego!")
        break
    destino = geocoding(loc2, key)

    print("=================================================")
    if origen[0] == 200 and destino[0] == 200:
        punto_origen = f"&point={origen[1]}%2C{origen[2]}"
        punto_destino = f"&point={destino[1]}%2C{destino[2]}"
        ruta_completa = f"{route_url}{urllib.parse.urlencode({'key': key, 'vehicle': vehiculo})}{punto_origen}{punto_destino}"
        ruta_data = requests.get(ruta_completa).json()
        ruta_status = requests.get(ruta_completa).status_code

        print(f"Estado del Routing API: {ruta_status}\nURL:\n{ruta_completa}")
        print("=================================================")
        print(f"Direcciones desde {origen[3]} hasta {destino[3]} usando '{vehiculo}'")
        print("=================================================")

        if ruta_status == 200:
            km = ruta_data["paths"][0]["distance"] / 1000
            miles = km / 1.61
            segundos = int(ruta_data["paths"][0]["time"] / 1000 % 60)
            minutos = int(ruta_data["paths"][0]["time"] / 1000 / 60 % 60)
            horas = int(ruta_data["paths"][0]["time"] / 1000 / 60 / 60)

            combustible = (km * 7.5) / 100

            print("Distancia recorrida: {:.2f} km / {:.2f} millas".format(km, miles))
            print("Duración del viaje: {:02d}:{:02d}:{:02d}".format(horas, minutos, segundos))
            print("Combustible consumido estimado: {:.2f} litros".format(combustible))
            print("=================================================")

            for paso in ruta_data["paths"][0]["instructions"]:
                texto = paso["text"]
                distancia_paso = paso["distance"] / 1000
                print("{0} ({1:.2f} km / {2:.2f} millas)".format(texto, distancia_paso, distancia_paso / 1.61))
            print("=================================================")
        else:
            print(f"Mensaje de error: {ruta_data['message']}")
            print("*************************************************")