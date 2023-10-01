# map_creator.py
import folium

m = folium.Map(location=[59.3293, 18.0686], zoom_start=10)
folium.Marker([59.3293, 18.0686], tooltip='Stockholm').add_to(m)
m.save('map.html')
