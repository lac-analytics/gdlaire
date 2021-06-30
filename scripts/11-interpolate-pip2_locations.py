import os
import sys
import geopandas as gpd
import pandas as pd
import numpy as np

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def main(start='2013/12/31', end='2019/12/31', save=False):

    #donwload data from databases
    query = f"SELECT * FROM data.simaj_data_day WHERE \"FECHA\" between \'{start}\' and \'{end}\'"
    df = aqiGDL.df_from_query(query)
    df['FECHA'] = pd.to_datetime(df['FECHA']).dt.date
    df.sort_values(by=['FECHA'], inplace=True)

    aqiGDL.log('Loaded air quality by day database')

    df_pip2 = pd.DataFrame(
        columns=['FECHA', 'PARAM', 'EST_PIP', 'CONC', 'LONG', 'LAT'])

    df_estaciones = aqiGDL.df_from_db('puntos_pip', 'estaciones')

    aqiGDL.log('Loaded PIP stations')

    df_estaciones.drop(columns=['geometry'], inplace=True)

    # avoid numbers and spaces in station names
    #df_estaciones['EST_MIMACRO'] = df_estaciones['Name'].str.split(" ", n=1, expand=True)[1]

    #aqiGDL.log('Created id column by PIP station database')

    empty0 = ''  # string used for logging empty values

    i = 0

    #interpolation
    for d in df.FECHA.unique():

        for p in df.PARAM.unique():

            for est in df_estaciones.Nombre.unique():
                
                # coordinates for interpolation
                long_int = df_estaciones.loc[df_estaciones.Nombre ==
                                             est]['Longitud'].iloc[0]
                lat_int = df_estaciones.loc[df_estaciones.Nombre ==
                                            est]['Latitud'].iloc[0]

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

                df_pip2.loc[i] = [d, p, est, c,
                                        long_int,
                                        lat_int
                                        ]

                if (i % 10000) == 0:

                    aqiGDL.log(f'Checkpoint, {i} iterations')

                i += 1

    aqiGDL.log('Created MiMacro DataFrame with interpolations')

    if save:

        aqiGDL.df_to_db(df_pip2, 'pip_data_day',
                        'data', if_exists='replace')

        aqiGDL.log('Uploaded database for PIP by day')


if __name__ == "__main__":

    main(save=True)
