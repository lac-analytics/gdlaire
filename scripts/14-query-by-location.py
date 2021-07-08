import os
import sys
import geopandas as gpd
import pandas as pd
import numpy as np
import osmnx as ox

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def location(lon, lat, name):

    gdf_point_user = pd.DataFrame({'name': name, "x": [lon], "y": [lat]})
    geometry_ = gpd.points_from_xy(gdf_point_user.x, gdf_point_user.y)

    gdf_point_user = gpd.GeoDataFrame(gdf_point_user, geometry=geometry_ ,crs="EPSG:4326")
    gdf_point_user = ox.project_gdf(gdf_point_user, to_crs='EPSG:32613')

    return gdf_point_user


def main(start='2013/12/31', end='2019/12/31', save=False):

    #donwload data from databases
    query = f"SELECT * FROM data.simaj_data_day WHERE \"FECHA\" between \'{start}\' and \'{end}\'"
    df = aqiGDL.df_from_query(query)
    df['FECHA'] = pd.to_datetime(df['FECHA']).dt.date
    df.sort_values(by=['FECHA'], inplace=True)

    aqiGDL.log('Loaded air quality by day database')

    df_mylocation_results = pd.DataFrame(
        columns=['FECHA', 'PARAM', 'NAME', 'CONC', 'LONG', 'LAT'])

    df_mylocation = location(lon, lat, name)

    aqiGDL.log('Loaded MiMacro stations')

    df_mylocation.drop(columns=['geometry'], inplace=True)

    # avoid numbers and spaces in station names
    df_mylocation['NAME'] = df_mylocation['NAME'].str.split(" ", n=1, expand=True)[1]

    aqiGDL.log('Created id column by MiMacro station database')

    empty0 = ''  # string used for logging empty values

    i = 0

    #interpolation
    for d in df.FECHA.unique():

        for p in df.PARAM.unique():

            for l in df_mylocation.NAME.unique():
                
                # coordinates for interpolation
                long_int = df_mylocation.loc[df_mylocation.NAME == l]['x'].iloc[0]
                lat_int = df_mylocation.loc[df_mylocation.NAME == l]['y'].iloc[0]

                simaj = df.loc[(df.FECHA == d) & (df.PARAM == p)]

                # interpolate concentration
                c = aqiGDL.interpolate_atpoint(
                    long_int, lat_int, simaj)

                if c == -1:

                    empty1 = (f'Empty value at parameter: {p}, date: {d}')

                    # checks if a parameter for a specified date is empty, so it doesn't repeat the log
                    if empty0 != empty1:

                        empty0 = empty1

                        aqiGDL.log(
                            f'Empty value at parameter: {p}, date: {d} and iteration: {i}')

                    c = np.nan

                df_mylocation_results.loc[i] = [d, p, l, c,
                                        long_int,
                                        lat_int
                                        ]

                if (i % 10000) == 0:

                    aqiGDL.log(f'Checkpoint, {i} iterations')

                i += 1

    aqiGDL.log('Created MiMacro DataFrame with interpolations')

    if save:

        aqiGDL.df_to_db(df_mylocation_results, 'mimacro_data_day',
                        'data', if_exists='replace')

        aqiGDL.log('Uploaded database for MiMacro by day')


if __name__ == "__main__":

    main(save=True)
