import folium
import pandas as pd
from folium.plugins import HeatMap
from fcn_localizacion import fcn_localizacion
from fcn_plot_ciudades_hub import plot_ciudades_hub

# Cargar datos desde el archivo Excel
df = pd.ExcelFile("Puntos_Loc.xlsx")
data = df.parse(sheet_name="Hoja1")
a = data['LONGITUD']
b = data['LATITUD']
w = data['PESOS']

# Problema de localización
optimal_x, optimal_y = fcn_localizacion(a, b, w)
y_hub = 36.672023 
x_hub = -4.551031

'''GRÁFICAS'''
plot_ciudades_hub(a, b, x_hub, y_hub, optimal_x, optimal_y)

'''MAPA CALOR'''
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

'''MAPA NORMAL'''
df = pd.ExcelFile("Clientes.xlsx")
data = df.parse(sheet_name="Hoja1")
# Crear un mapa centrado en la ubicación promedio
mapa_normal = folium.Map(location=[data['LATITUD'].mean(), data['LONGITUD'].mean()], zoom_start=12)

# Agregar marcadores para cada tienda
for _, row in data.iterrows():
    folium.Marker(
        location=[row['LATITUD'], row['LONGITUD']],
        popup=f"Tienda: {row['NOMBRE']}",  # Asegúrate de que exista una columna 'Nombre' en tu archivo Excel
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