from retriever import DataRetriever
from constants import BASE_URL, QUERY_PARAMETERS, PAGINATION_KEY
import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster

if __name__ == "__main__":

    if not os.path.isfile('results/records_all_pages.csv'):
        os.makedirs('results') 
        data_retriever = DataRetriever(BASE_URL, query_params=QUERY_PARAMETERS, pagination_key=PAGINATION_KEY)
        records_all_pages = []
        for data in data_retriever.retrieve_information():
            # implement parser
            records_page_dicts = data.json().get("result", {}).get("records")
            records_all_pages.extend(records_page_dicts)
        records_all_pages_df = pd.DataFrame(records_all_pages)
        records_all_pages_df.set_index('_id', inplace=True)
        records_all_pages_df.rename_axis('id', inplace=True)
        print('All bedbugs records MTL df:', '\n', records_all_pages_df, '\n')
        print('Total number of records pulled:', len(records_all_pages_df), '\n')
        print('Variables in each record ...', '\n', records_all_pages_df.columns, '\n')
        #Save this to a csv to avoid having to repull the data.
        print("Saving all MTL bedbugs records to 'results/records_all_pages.csv'")
        records_all_pages_df.to_csv('results/records_all_pages.csv')
    else:
        print("Loading all MTL bedbugs records from 'results/records_all_pages.csv'", '\n')
        records_all_pages_df = pd.read_csv('results/records_all_pages.csv')

    # Initialize the interactive folium map centered around Montreal
    m = folium.Map(location=[45.5017, -73.5673], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)

    # Add points/clusters to the map
    for idx, row in records_all_pages_df.iterrows():
        folium.CircleMarker(
            location=[float(row['LATITUDE']), float(row['LONGITUDE'])], 
            radius=1, # Defines the radius of the circle marker in pixels.
            color="red", # The color of the marker's edge
            fill=True,
            fill_color="red" # The fill color of the marker
        ).add_to(marker_cluster)
    # Save the map to an html
    print("Saving interactive MTL bedbugs cluster map to 'results/bed_bugs_mtl_clustermap'")
    m.save('results/bed_bugs_mtl_clustermap.html')
