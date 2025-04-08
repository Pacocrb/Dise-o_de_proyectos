from folium.plugins import HeatMap
import folium
def heat_map(data, y_hub, x_hub):
    # Crear un mapa centrado en la ubicación promedio
    mapa = folium.Map(location=[data['LATITUD'].mean(), data['LONGITUD'].mean()], zoom_start=12)

    # Preparar datos para el mapa de calor (lista de [latitud, longitud])
    heat_data = data[['LATITUD', 'LONGITUD']].values.tolist()

    # Agregar el mapa de calor al mapa principal  
    HeatMap(heat_data).add_to(mapa)

    # Agregar marcador del hub al mapa de calor
    folium.Marker(
        location=[y_hub, x_hub],
        popup="Hub Actual",
        icon=folium.Icon(color='red', icon='star')
    ).add_to(mapa)

    # Guardar el mapa interactivo
    mapa.save("mapa_calor_clientes.html")