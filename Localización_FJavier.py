import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap, MarkerCluster
from shapely.geometry import Point

# 1. Cargar datos
df = pd.read_excel("Clientes.xlsx")

# 2. Filtrar por la zona de interés (entre Manilva y Nerja)
longitud_min = -5.4  # Extremo más occidental (Manilva)
longitud_max = -3.8  # Extremo más oriental (Nerja)

lat_min, lat_max = 36.5, 37.15
lon_min, lon_max = -5.48, -3.90

df_filtrado = df[(df['Latitud'] >= lat_min) & (df['Latitud'] <= lat_max) &
(df['Longitud'] >= lon_min) & (df['Longitud'] <= lon_max)]

# 3. Convertir a GeoDataFrame para análisis espacial
geometry = [Point(xy) for xy in zip(df_filtrado['Longitud'], df_filtrado['Latitud'])]
gdf = gpd.GeoDataFrame(df_filtrado, geometry=geometry)

# 4. Análisis de clustering para encontrar ubicaciones óptimas
X = df_filtrado[['Longitud', 'Latitud']].values
num_centros = 1  # Ajusta el número de clusters según sea necesario
kmeans = KMeans(n_clusters=num_centros, random_state=42, n_init=10)
df_filtrado['cluster'] = kmeans.fit_predict(X)
centros = kmeans.cluster_centers_

# 5. Calcular el centroide promedio
centroide_promedio = df_filtrado[['Longitud', 'Latitud']].mean().values

# 6. Visualizar resultados
mapa = folium.Map(location=[df_filtrado['Latitud'].mean(), df_filtrado['Longitud'].mean()], zoom_start=12)

# Añadir mapa de calor
heat_data = df_filtrado[['Latitud', 'Longitud']].values.tolist()
HeatMap(heat_data).add_to(mapa)

# Añadir clusters
colores = ['red', 'blue', 'green', 'purple', 'orange', 'darkred']
marker_cluster = MarkerCluster().add_to(mapa)

for i, centro in enumerate(centros):
    cluster_points = df_filtrado[df_filtrado['cluster'] == i]
    
    for _, punto in cluster_points.iterrows():
        folium.CircleMarker(
            location=[punto['Latitud'], punto['Longitud']],
            radius=3,
            color=colores[i % len(colores)],
            fill=True,
            fill_opacity=0.7,
            popup=punto.get('Name', f"Punto {_}")
        ).add_to(marker_cluster)
    
    folium.Marker(
        location=[centro[1], centro[0]],
        icon=folium.Icon(color=colores[i % len(colores)], icon='star'),
        popup=f'Centro logístico {i+1}'
    ).add_to(mapa)

# Añadir el centroide promedio general
folium.Marker(
    location=[centroide_promedio[1], centroide_promedio[0]],
    icon=folium.Icon(color='black', icon='home'),
    popup='Centro logístico global (promedio)'
).add_to(mapa)

folium.LayerControl().add_to(mapa)

# Guardar y mostrar mapa
mapa.save('mapa.html')
