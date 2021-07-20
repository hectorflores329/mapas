from flask import Flask
import folium
import folium.plugins as plugins
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from folium.plugins import FloatImage
from folium.plugins import Draw
from folium.plugins import MiniMap

app = Flask(__name__)

@app.route('/')
def mapa():

    _data = pd.DataFrame({
        'lat':[-18.523171602611157, -20.081406746064033, -23.59873676994002, -27.23938743975787, -29.96370275016499, -33.047173911560314, -33.43809989010958, -34.39381185918305, -35.44477628689832, -36.595441980200604, -37.28730334091126, -38.70563226104338, -40.01699278867277, -41.03688009107713, -45.73070038865504, -52.2166525002859462],
        'lon':[-69.63145087536489, -69.43448162427181, -70.38826103180747, -69.7905950891039, -71.29217004776821, -71.62392382162052, -70.62712736036686, -71.17591266489721, -71.40116279394256, -72.02111747509933, -72.46656376159729, -72.23016045899877, -72.64926437255212, -73.1082958286221, -72.79822387430552, -72.1980173424485],
        'name':['Región de Arica y Parinacota', 'Región de Tarapacá', 'Región de Antofagasta.', 'Región de Atacama', 'Región de Coquimbo', 'Región de Valparaíso', 'Región Metropolitana de Santiago', 'Región del Libertador General Bernardo O’Higgin', 'Región del Maule', 'Región del Ñuble', 'Región del Biobío', 'Región de La Araucanía', 'Región de Los Río', 'Región de Los Lagos', 'Región de Aysén del General Carlos Ibáñez del Campo', 'Región de Magallanes y la Antártica Chilena'],
        'value':[10, 12, 40, 70, 23, 43, 100, 43, 90, 100, 11, 48, 79, 82, 49, 17]
    })

    np.random.seed(3141592)
    initial_data = np.random.normal(size=(100, 2)) * np.array([[1, 1]]) + np.array(
        [[-33.48621795345005, -70.66557950912359]]
    )

    move_data = np.random.normal(size=(100, 2)) * 0.01

    data = [(initial_data + move_data * i).tolist() for i in range(100)]

    time_index = [
        (datetime.now() + k * timedelta(1)).strftime("%Y-%m-%d") for k in range(len(data))
    ]

    weight = 1  # default value
    for time_entry in data:
        for row in time_entry:
            row.append(weight)

    # atlas = folium.raster_layers.WmsTileLayer(url = 'https://ide.dataintelligence-group.com/geoserver/chile/wms?', layers='chile:Regiones', name='test', fmt='image/png', attr='test', transparent=True, version='1.3.0')

    m = folium.Map(
        location=[-33.48621795345005, -70.66557950912359],
        zoom_start=5,
        min_zoom = 8,
        max_zoom = 30,
        control_scale=True
        # tiles = "openstreetmap"
        )

    w = folium.WmsTileLayer(url = 'https://ide.dataintelligence-group.com/geoserver/chile/wms',
                        layers = 'chile:Regiones',
                        fmt ='image/png',
                        transparent = True,
                        name = "Regiones",
                        control = True,
                        attr = "Mapa de Chile",
                        overlay=True,
                        control=True,
                        show=True
                        )

    w.add_to(m)

    hm = plugins.HeatMapWithTime(data, index=time_index, name="Puntos", auto_play=True, max_opacity=0.3, position='bottomright')

    hm.add_to(m)
    
    '''folium.Marker(
        location=[-33.48621795345005, -70.66557950912359],
        popup="Esto es una marca estática.",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)

    folium.CircleMarker(
        location=[-33.047971387856414, -71.61855844930044],
        radius=50,
        popup="Circunferencia estática ubicada en Valparaíso.",
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(m)'''

    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.LayerControl().add_to(m)

    url = (
        "https://github.com/hectorflores329/herokuinstance/raw/main/dataintelligence.png"
    )

    FloatImage(url, bottom=1, left=8).add_to(m)

    draw = Draw(export=True)

    draw.add_to(m)

    minimap = MiniMap(toggle_display=True)
    minimap.add_to(m)

    for i in range(0,len(_data)):
        folium.Marker(
            location = [_data.iloc[i]['lat'], _data.iloc[i]['lon']],
            popup =_data.iloc[i]['name'],
            name="Puntos, regiones chilenas",
        ).add_to(m)

    return m._repr_html_()
    # return HeatMapWithTime(lat_long_list2,radius=5,auto_play=True,position='bottomright').add_to(map)

if __name__ == '__main__':
    app.run()
