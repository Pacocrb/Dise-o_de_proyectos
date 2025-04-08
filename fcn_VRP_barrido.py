import folium
import numpy as np
from math import atan2, degrees

def VRP_barrido(data, deposito, y_hub, x_hub):
    # Calcular distancia y ángulo polar desde el depósito
    def calcular_angulo(long1, lat1, long2, lat2):
        delta_x = long2 - long1
        delta_y = lat2 - lat1
        return degrees(atan2(delta_y, delta_x)) % 360

    data['Ángulo'] = data.apply(
        lambda row: calcular_angulo(deposito['Longitude'], deposito['Latitude'], row['Longitude'], row['Latitude']),
        axis=1
    )

    # Ordenar por ángulo
    data = data.sort_values(by='Ángulo')

    # Agrupar por capacidad del vehículo
    capacidad_vehiculo = 50
    rutas = []
    ruta_actual = []
    carga_actual = 0
    # Algoritmo de barrido
    for _, row in data.iterrows():
        if carga_actual + row['Demanda'] > capacidad_vehiculo:
            # Cerrar la ruta regresando al depósito
            ruta_actual.insert(0, deposito['Nombre'])  # Añadir depósito al inicio
            ruta_actual.append(deposito['Nombre'])    # Añadir depósito al final
            rutas.append(ruta_actual)
            # Reiniciar ruta
            ruta_actual = []
            carga_actual = 0
        # Añadir tienda a la ruta actual
        ruta_actual.append(row['Name'])
        carga_actual += row['Demanda']

    # Añadir la última ruta si queda alguna pendiente
    if ruta_actual:
        ruta_actual.insert(0, deposito['Nombre'])
        ruta_actual.append(deposito['Nombre'])
        rutas.append(ruta_actual)

    # Mostrar rutas generadas
    for i, ruta in enumerate(rutas, start=1):
        print(f"Ruta {i}: {ruta}")

    mapa = folium.Map(location=[deposito['Latitude'], deposito['Longitude']], zoom_start=12)

    # Añadir puntos y rutas
    for i, ruta in enumerate(rutas):
        color = f"#{np.random.randint(0, 0xFFFFFF):06x}"  # Colores aleatorios
        puntos = []
        for nombre in ruta:
            if nombre == 'Depósito':
                punto = [deposito['Latitude'], deposito['Longitude']]
            else:
                # Verificar si el nombre está en el DataFrame
                if not data[data['Name'] == nombre].empty:
                    fila = data[data['Name'] == nombre].iloc[0]
                    punto = [fila['Latitude'], fila['Longitude']]
                else:
                    print(f"Advertencia: La tienda '{nombre}' no se encuentra en los datos.")
                    continue
            puntos.append(punto)
            folium.Marker(location=punto, popup=nombre, icon=folium.Icon(color="blue")).add_to(mapa)
        folium.PolyLine(puntos, color=color, weight=2.5, opacity=1).add_to(mapa)

    # Agregar marcador del hub al mapa de calor
    folium.Marker(
        location=[y_hub, x_hub],
        popup="Hub Actual",
        icon=folium.Icon(color='red', icon='star')
    ).add_to(mapa)

    # Mostrar mapa
    mapa.save("rutas_barrido.html")