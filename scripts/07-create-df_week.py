import os
import sys
import geopandas as gpd
import pandas as pd

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL



def main(station, start='2013/12/31', end='2019/12/31', save=False):

    query = f"SELECT * FROM data.{station.lower()}_data_day WHERE \"FECHA\" between \'{start}\' and \'{end}\'"
    df = aqiGDL.df_from_query(query)
    df['FECHA'] = pd.to_datetime(df['FECHA']).dt.date
    df.sort_values(by=['FECHA'], inplace=True)

    aqiGDL.log('Loaded air quality by day database')

    df_week = aqiGDL.week_average (df, station)

    aqiGDL.log(f'Created air quality database by week for {station}')

    if save:

        aqiGDL.df_to_db(df_week, station.lower()+'_data_week', 'data', if_exists='replace')
        
        aqiGDL.log(f'Uploaded database for station: {station}')
    


if __name__ == "__main__":
    
    main('MIMACRO', save=True)