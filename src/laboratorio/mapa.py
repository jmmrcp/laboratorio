import folium
import pandas as pd
from folium.plugins import MarkerCluster, MousePosition
from folium.features import DivIcon

# 1. Cargamos los datos con las coordenadas
URL = 'spacex_launch_geo.csv'
spacex_df = pd.read_csv(URL)

# 2. Inicializamos el mapa con tema oscuro (CartoDB dark_matter) para que combine con el Dashboard
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5, tiles='cartodbdark_matter')

# 3. Preparamos el agrupador de marcadores
marker_cluster = MarkerCluster()
site_map.add_child(marker_cluster)

# 4. Asignamos colores corporativos
def assign_marker_color(launch_outcome):
    return '#00e676' if launch_outcome == 1 else '#ff5252' # Verde Neón y Rojo Carmesí
    
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)

# 5. Poblamos el mapa con popups enriquecidos
for index, record in spacex_df.iterrows():
    # Creamos un popup HTML con estilo para cuando el usuario haga clic
    html_popup = f"""
    <div style="font-family: Arial; color: #333;">
        <b>Base:</b> {record['Launch Site']}<br>
        <b>Resultado:</b> {'Éxito' if record['class'] == 1 else 'Fracaso'}
    </div>
    """
    
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color']),
        popup=folium.Popup(html_popup, max_width=200)
    )
    marker_cluster.add_child(marker)

# 6. EXPORTACIÓN A PRODUCCIÓN: Guardamos el mapa interactivo como archivo web
# Este archivo puede ser servido online o incluido en la carpeta 'assets' de Plotly Dash
site_map.save("assets/mapa_spacex.html")
print("Mapa interactivo generado exitosamente en: assets/mapa_spacex.html")