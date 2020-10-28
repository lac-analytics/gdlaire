# Download the graph to disk

import geopandas as gpd
import os
import sys
import osmnx as ox
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def main(filename, folder, schema, table_name):
    gdf = gpd.read_file(f'../data/{folder}/{filename}')
    aqiGDL.log('Polygon loaded')
    aqiGDL.gdf_to_db(gdf, name=table_name, schema=schema)


if __name__ == "__main__":
    # File to upload
    filename = 'estaciones_MiMacroPeriferico.geojson'
    # Location in data folder
    folder = 'external'
    # Schema in where to save the file in the DB
    schema = 'Estaciones'
    # Nombre de la tabla a crear
    table_name = 'estaciones_gdl'
    main(filename, folder, schema, table_name)
