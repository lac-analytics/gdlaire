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

    query = f"SELECT * FROM data.simaj_data_day WHERE \"FECHA\" between \'{start}\' and \'{end}\'"
    df = aqiGDL.df_from_query(query)
    df['FECHA'] = pd.to_datetime(df['FECHA']).dt.date
    df.sort_values(by=['FECHA'], inplace=True)

    aqiGDL.log('Loaded air quality by day database')

    df_mimacro = pd.DataFrame(
        columns=['FECHA', 'PARAM', 'EST_MIMACRO', 'CONC', 'LONG', 'LAT'])

    df_estaciones = aqiGDL.df_from_db('estaciones_gdl', 'estaciones')

    aqiGDL.log('Loaded MiMacro stations')

    df_estaciones.drop(columns=['geometry'], inplace=True)

    for i in range(0, len(df)):
        df_estaciones['pos'] = df_estaciones.Name.str.find('.')
        df_estaciones.EST_MIMACRO = df_estaciones.apply(
            lambda x: x.Name[0:x['pos']], axis=1)

    df_estaciones.drop(columns=['pos'], inplace=True)

    aqiGDL.log('Created id column by MiMacro station database')

    i = 0

    for d in df.FECHA.unique():

        for p in df.PARAM.unique():

            for est in df_estaciones.EST_MIMACRO.unique():

                long_int = df_estaciones.loc[df_estaciones.EST_MIMACRO ==
                                             est]['x'].iloc[0]
                lat_int = df_estaciones.loc[df_estaciones.EST_MIMACRO ==
                                            est]['y'].iloc[0]

                simaj = df.loc[(df.FECHA == d) & (df.PARAM == p)]

                c = aqiGDL.interpolate_atpoint(
                    long_int, lat_int, simaj)

                if c == -1:

                    aqiGDL.log(
                        f'Empty value at parameter: {p}, date: {d} and iteration: {i}')

                    df_mimacro.loc[i] = [d, p, est, np.nan,
                                         long_int,
                                         lat_int
                                         ]

                else:

                    df_mimacro.loc[i] = [d, p, est, c,
                                         long_int,
                                         lat_int
                                         ]

                if (i % 10000) == 0:

                    aqiGDL.log(f'Checkpoint, {i} iterations')

                i += 1

    aqiGDL.log('Created MiMacro DataFrame with interpolations')

    if save:

        aqiGDL.df_to_db(df_mimacro, 'mimacro_data_day',
                        'data', if_exists='replace')

        aqiGDL.log('Uploaded database for MiMacro by day')


if __name__ == "__main__":

    main(save=True)
