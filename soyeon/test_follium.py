import folium
import sqlite3
import pandas as pd


con = sqlite3.connect('../database/seoul_db.db')
df_food = pd.read_sql('SELECT * FROM food_list', con)



def sample_func(guname):
    # Create a map object
    map = folium.Map(location=[37.564214, 127.001699], zoom_start=11)

    lodge_query = pd.read_sql(
        f"SELECT 사업장명, 도로명주소, 전화번호, x_pos, y_pos, img_path FROM seoul_lodges WHERE 도로명주소 LIKE '%{guname}%'", con)
    cnt = 0
    for index, row in lodge_query.iterrows():
        cnt += 1
        print(index, row)
        x_pos = row['x_pos']
        y_pos = row['y_pos']
        name = row['사업장명']
        # info = row['도로명주소'], row['전화번호']
        # img = row['img_path']

        marker1 = folium.Marker(location=[x_pos, y_pos], popup=name)
        marker1.add_to(map)
    print(cnt)

    map.save('map.html')
    map.show_in_browser()

    # Clear the markers from the map
    for i in range(cnt):
        map.get_root().html.add_child(folium.Element(f'<script>document.getElementsByClassName("leaflet-marker-icon")[{i}].style.display="none";</script>'))

    # Save the updated map
    map.save('map_updated.html')

sample_func('강북구')