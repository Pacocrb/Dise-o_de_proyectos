import folium
import pandas as pd
import numpy as np
from folium.plugins import HeatMap
from fcn_localizacion import fcn_localizacion
from fcn_plot_ciudades_hub import plot_ciudades_hub
from fcn_heat_map import heat_map
from fcn_plot_clientes_depot import plot_clientes_depot
from fcn_VRP_barrido import VRP_barrido
from fcn_VRP_NN import VRP_vecino

'''Problema de localización'''
# Cargar datos desde el archivo Excel
df = pd.ExcelFile("Puntos_Loc.xlsx")
data_loc = df.parse(sheet_name="Hoja1")
a = data_loc['LONGITUD']
b = data_loc['LATITUD']
w = data_loc['PESOS']
# optimal_x, optimal_y = fcn_localizacion(a,b,w)
y_hub = 36.672023 
x_hub = -4.551031
# plot_ciudades_hub(a, b, x_hub, y_hub, optimal_x, optimal_y)
# heat_map(data_loc, y_hub, x_hub)

'''Problema de VRP'''
# df = pd.ExcelFile("Clientes_malaga_v2.xlsx")
# data_raw = df.parse(sheet_name="Hoja1")
# # Filtrar tiendas dentro de los límites de la provincia de Málaga
# lat_min, lat_max = 36.5, 37.15
# lon_min, lon_max = -5.48, -3.90
# data = data_raw[
#     (data_raw['Latitude'] >= lat_min) & (data_raw['Latitude'] <= lat_max) &
#     (data_raw['Longitude'] >= lon_min) & (data_raw['Longitude'] <= lon_max)
# ]
# data.to_excel('clientes_definitivos.xlsx', index=False, engine='openpyxl')
# df = pd.ExcelFile("clientes_definitivos.xlsx")
# data0 = df.parse(sheet_name="Sheet1")
# data = data0.sample(n=100, random_state=42)
# data.to_excel('clientes_definitivos_filtrados.xlsx', index=False, engine='openpyxl')

df = pd.ExcelFile("clientes_definitivos_filtrados.xlsx")
data = df.parse(sheet_name="Sheet1")
plot_clientes_depot(data, x_hub, y_hub)

# Generar demanda de las tiendas, actualizar a valores reales
data['Demanda'] = np.random.randint(4, 8, size=len(data))
# Definir coordenadas del depósito
deposito = {'Nombre': 'Depósito', 'Longitude': x_hub, 'Latitude': y_hub}
capacidad_vehiculo = 50

VRP_barrido(data, deposito, y_hub, x_hub, capacidad_vehiculo)
VRP_vecino(data, deposito, y_hub, x_hub, capacidad_vehiculo)

print('Fin del codigo')