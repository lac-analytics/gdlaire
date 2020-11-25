import os
import sys
import geopandas as gpd
import pandas as pd

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def main(interval='day', save=False):

    simaj_data = aqiGDL.restructure_database(interval = interval)

    aqiGDL.log('Restructure database')

    if save:

        aqiGDL.df_to_db(simaj_data, 'simaj_data_'+interval, 'data', if_exists='replace')
        
        aqiGDL.log(f'Uploaded database for interval: {interval}')
    


if __name__ == "__main__":
    
    main(save=True)
