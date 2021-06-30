import os
import sys
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL

url = 'airegdlpip.cptlhu1n34ei.us-west-1.rds.amazonaws.com'
user = 'postgres'
pw = 'pipguadalajara'
db = 'postgres'


def db_engine():
    """Function to create an engine with Ada

    Returns:
        database engine: sqlalchemy engine
    """
    aqiGDL.log('Creating SQL engine')
    return create_engine("postgresql://{user}:{pw}@{url}/{db}".format(user=str(
        user), pw=str(pw), url=str(url), db=str(db)))


def df_from_db(name, schema):
    """Load a table from the database into a DataFrame

    Args:
        name (str): Name of the table to be loaded
        schema (str): Name of the folder from where to load the geoDataFrame

    Returns:
        pandas.DataFrame: GeoDataFrame with the table from the database.
    """
    engine = db_engine()
    aqiGDL.log(f'Getting {name} from DB')
    df = pd.read_sql(
        f"SELECT * FROM {schema.lower()}.{name.lower()}", engine)
    aqiGDL.log(f'{name} retrived')
    return df


def gdf_from_db(name, schema):
    """Load a table from the database into a GeoDataFrame

    Args:
        name (str): Name of the table to be loaded
        schema (str): Name of the folder from where to load the geoDataFrame

    Returns:
        geopandas.GeoDataFrame: GeoDataFrame with the table from the database.
    """
    engine = db_engine()
    aqiGDL.log(f'Getting {name} from DB')
    gdf = gpd.read_postgis(
        f"SELECT * FROM {schema.lower()}.{name.lower()}", engine, geom_col='geometry')
    aqiGDL.log(f'{name} retrived')
    return gdf


def main(schema, table):
    if schema == 'data':
        df = df_from_db(table, schema)
        aqiGDL.df_to_db(df, table, schema)
        aqiGDL.log(f'{schema}.{table} migrated')
    else:
        gdf = gdf_from_db(table, schema)
        aqiGDL.gdf_to_db(gdf, table, schema)
        aqiGDL.log(f'{schema}.{table} migrated')


if __name__ == '__main__':
    tables = {'data': ['mimacro_data_day', 'mimacro_data_week', 'simaj_data_day', 'simaj_data_hour',
                       'simaj_data_week'], 'estaciones': ['estaciones_gdl'], 'estaciones_simaj': ['estaciones_simaj']}

    for k, v in tables.items():
        for table in v:
            main(k, table)

    aqiGDL.log(f'All done.')
