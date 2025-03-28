import folium
import pandas as pd
import numpy as np
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import contextily as ctx
from scipy.optimize import minimize

# Cargar datos desde el archivo Excel
df = pd.ExcelFile("Puntos_Loc.xlsx")
data = df.parse(sheet_name="Hoja1")
a = data['LONGITUD']
b = data['LATITUD']
w = data['PESOS']

# Gráfica en ejes estandar

x_min = np.min(data['LONGITUD']) 
x_max = np.max(data['LONGITUD'])
y_min = np.min(data['LATITUD']) 
y_max = np.max(data['LATITUD'])

# Definir los rangos para x e y (en este caso, se escalarán proporcionalmente)
# x = (data['LONGITUD'] - x_min) / (x_max - x_min) * 100  # Escalar la longitud
# y = (data['LATITUD'] - y_min) / (y_max - y_min) * 100   # Escalar la latitud

# plt.figure(1)
# plt.scatter(x,y, marker='o', s=30,edgecolors='blue',facecolor='none')
# plt.title('Tiendas de electrodomésticos en la provincia de Málaga', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# # plt.xlabel('[m]', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
# # plt.ylabel('[m]', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
# plt.minorticks_on()
# plt.grid(True, which='major', linewidth=0.5, color='gray', linestyle='-', alpha=0.7)  # Rejilla principal
# plt.grid(True, which='minor', linewidth=0.2, color='black', linestyle=':', alpha=0.5)  # Rejilla menor
# plt.show()

# Gráfica en ejes de mapas
'''Método de localización'''
# Función a minimizar
def weighted_distance(params):
    x, y = params
    return np.sum(w * np.sqrt((x - a)**2 + (y - b)**2))

# Punto inicial para la optimización
x_grav = sum(w*a) / sum(w)
y_grav = sum(w*b) / sum(w)
initial_guess = [x_grav, y_grav]

# Optimización
result = minimize(weighted_distance, initial_guess)

# Solución óptima
optimal_x, optimal_y = result.x
print(f"Coordenadas óptimas: x = {optimal_x}, y = {optimal_y}")

y_hub = 36.672023 
x_hub = -4.551031

plt.figure(2)
plt.scatter(a,b, marker='o', s=30,edgecolors='blue',facecolor='none')
plt.scatter(x_hub,y_hub, marker='o', s=30,edgecolors='red',facecolor='none')
plt.scatter(optimal_x,optimal_y, marker='o', s=30,edgecolors='purple',facecolor='none')
plt.title('Tiendas de electrodomésticos en la provincia de Málaga', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Longitud', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
plt.ylabel('Latitud', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
plt.minorticks_on()
plt.grid(True, which='major', linewidth=0.5, color='gray', linestyle='-', alpha=0.7)  # Rejilla principal
plt.grid(True, which='minor', linewidth=0.2, color='black', linestyle=':', alpha=0.5)  # Rejilla menor
plt.show()



# # Crear un mapa centrado en la ubicación promedio
# mapa = folium.Map(location=[data['Latitud'].mean(), data['Longitud'].mean()], zoom_start=12)

# # Preparar datos para el mapa de calor (lista de [latitud, longitud])
# heat_data = data[['Latitud', 'Longitud']].values.tolist()

# # Agregar el mapa de calor al mapa principal
# HeatMap(heat_data).add_to(mapa)

# # Guardar el mapa interactivo
# mapa.save("mapa_calor_clientes.html")

# # Crear un mapa centrado en la ubicación promedio
# mapa_normal = folium.Map(location=[data['Latitud'].mean(), data['Longitud'].mean()], zoom_start=12)

# # Agregar marcadores para cada tienda
# for _, row in data.iterrows():
#     folium.Marker(
#         location=[row['Latitud'], row['Longitud']],
#         popup=f"Tienda: {row['Nombre']}",  # Asegúrate de que exista una columna 'Nombre' en tu archivo Excel
#         icon=folium.Icon(color='blue', icon='info-sign')
#     ).add_to(mapa_normal)

# # Guardar el mapa interactivo
# mapa_normal.save("mapa_tiendas.html")