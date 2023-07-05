# # --- folium 마커 찍기 테스트
# folium.Marker([latitude, longitude],
#               radius=30,
#               tooltip="윤재 집",
#               popup='<iframe width="560" height="315" src="https://www.youtube.com/embed/dpwTOQri42s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
#               icon=folium.Icon(color="red", icon="info-sign")
#               ).add_to(m)

# # ----- folium MarkerCluster / Sub DataFrame
# sub_df = self.df_tour.loc[self.df_tour['map_select'].isin([1])]
# matching = sub_df[['x_pos', 'y_pos']]

# ----- 다른 방법
# for lat, long in zip(matching['x_pos'], matching['y_pos']):
#     folium.Marker([lat, long],
#                   tooltip="",
#                   icon=folium.Icon(color="red")
#                   ).add_to(marker_cluster)