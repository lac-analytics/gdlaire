# Download the graph to disk

import geopandas as gpd
import os
import sys
import osmnx as ox
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def main(city, save=False):
    polygon = gpd.read_file(f'../data/raw/{city}_area.geojson')
    aqiGDL.log('Polygon loaded')
    aqiGDL.gdf_to_db(polygon, city, schema='areas')


if __name__ == "__main__":
    city = 'Guadalajara'
    main(city, save=True)
