from math import radians, sin, cos, sqrt, atan2
import folium
import numpy as np

def VRP_vecino(data, deposito, y_hub, x_hub, capacidad_vehiculo):
    # Calcular la distancia entre dos puntos geográficos
    def calcular_distancia(lat1, lon1, lat2, lon2):
        # Radio de la Tierra en kilómetros
        R = 6371.0
        # Convertir coordenadas a radianes
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    # Implementación del algoritmo del vecino más cercano
    def vecino_mas_cercano(data, deposito, capacidad_vehiculo):
        # Crear lista de clientes
        clientes = data[['Name', 'Latitude', 'Longitude', 'Demanda']].to_dict('records')
        # Lista para guardar las rutas
        rutas = []
        # Mientras queden clientes por visitar
        while clientes:
            ruta_actual = []
            carga_actual = 0
            # Punto de partida: el depósito
            actual = {'Name': deposito['Nombre'], 'Latitude': deposito['Latitude'], 'Longitude': deposito['Longitude']}
            ruta_actual.append(actual['Name'])
            # Construir la ruta
            while clientes:
                # Calcular distancias a los clientes restantes
                distancias = [
                    (cliente, calcular_distancia(actual['Latitude'], actual['Longitude'], cliente['Latitude'], cliente['Longitude']))
                    for cliente in clientes
                ]
                # Seleccionar el cliente más cercano
                cliente_mas_cercano, distancia = min(distancias, key=lambda x: x[1])
                # Verificar capacidad del vehículo
                if carga_actual + cliente_mas_cercano['Demanda'] > capacidad_vehiculo:
                    break
                # Agregar cliente a la ruta
                ruta_actual.append(cliente_mas_cercano['Name'])
                carga_actual += cliente_mas_cercano['Demanda']
                # Actualizar el punto actual y eliminar cliente de la lista
                actual = cliente_mas_cercano
                clientes.remove(cliente_mas_cercano)
            # Cerrar la ruta regresando al depósito
            ruta_actual.append(deposito['Nombre'])
            rutas.append(ruta_actual)
        return rutas

    # Ejecutar el algoritmo
    rutas_nna = vecino_mas_cercano(data, deposito, capacidad_vehiculo)

    # # Mostrar las rutas generadas
    # for i, ruta in enumerate(rutas_nna, start=1):
    #     print(f"Ruta {i}: {ruta}")

    # Visualizar las rutas en el mapa
    mapa_nna = folium.Map(location=[deposito['Latitude'], deposito['Longitude']], zoom_start=12)

    for i, ruta in enumerate(rutas_nna):
        color = f"#{np.random.randint(0, 0xFFFFFF):06x}"  # Colores aleatorios
        puntos = []
        for nombre in ruta:
            if nombre == 'Depósito':
                puntos.append([deposito['Latitude'], deposito['Longitude']])
            else:
                fila = data[data['Name'] == nombre].iloc[0]
                puntos.append([fila['Latitude'], fila['Longitude']])
                folium.Marker(location=[fila['Latitude'], fila['Longitude']], popup=nombre, icon=folium.Icon(color="blue")).add_to(mapa_nna)
        folium.PolyLine(puntos, color=color, weight=2.5, opacity=1).add_to(mapa_nna)

    # Agregar el marcador del depósito al mapa
    folium.Marker(
        location=[y_hub, x_hub],
        popup="Hub Actual",
        icon=folium.Icon(color='red', icon='star')
    ).add_to(mapa_nna)

    # Guardar el mapa interactivo
    mapa_nna.save("rutas_nna.html")
