import folium

def plot_clientes_depot(data,x_hub,y_hub):
    # Crear un mapa centrado en la ubicación promedio
    mapa_normal = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=12)

    # Agregar marcadores para cada tienda
    for _, row in data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Tienda: {row['Name']}",  # Asegúrate de que exista una columna 'Nombre' en tu archivo Excel
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(mapa_normal)

    # Agregar marcador del hub al mapa de tiendas
    folium.Marker(
        location=[y_hub, x_hub],
        popup="Hub Actual",
        icon=folium.Icon(color='red', icon='star')
    ).add_to(mapa_normal)

    # Guardar el mapa interactivo
    mapa_normal.save("mapa_tiendas.html")