import os
import sys
import requests
import geopandas as gpd
import pandas as pd
import numpy as np

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def main():

    url = "https://api.smartcitizen.me/v0/search?q=PIPCiudadFuturo"
    response = requests.get(url).json()

    aqiGDL.log(
            'Downloaded data from Smart Citizen with the tag PIPCiudadFuturo')

    df_pip = pd.json_normalize(response)

    df_sck = pd.DataFrame()

    #iterate devices with the tag PIPCiudadFuturo
    for d in df_pip.loc[df_pip.type=='Device']['id']:
        
        url_device = f'https://api.smartcitizen.me/v0/devices/{d}'
        response_device = requests.get(url_device).json()

        aqiGDL.log(
            f'Downloaded measurement data for the device {d}')

        df_device = pd.json_normalize(response_device['data']['sensors'])
        
        df_location = pd.json_normalize(response_device['data']['location'])
        lat = df_location['latitude'].values[0]
        lon = df_location['longitude'].values[0]
        
        #iterate over sensors for each device
        for s in df_device.id.unique():
            
            url_mes = f'https://api.smartcitizen.me/v0/devices/{d}/readings?sensor_id={s}&rollup=1h'
            response_mes = requests.get(url_mes).json()

            aqiGDL.log(
            f'Downloaded measurement data for the device: {d} and sensor: {s}')

            df_mes = pd.json_normalize(response_mes, 'readings')
            
            df_mes.rename(columns={0:'date',1:'value'}, inplace=True)
            df_mes['device_id'] = d
            df_mes['param'] = df_device.loc[df_device.id==s]['description'].values[0]
            df_mes['unit'] = df_device.loc[df_device.id==s]['unit'].values[0]
            df_mes['lon'] = lon
            df_mes['lat'] = lat
            
            df_sck = df_sck.append(df_mes)

    # to GeoDataframe
    gdf_sck = gpd.GeoDataFrame(df_sck, geometry=gpd.points_from_xy(
                df_sck.lon, df_sck.lat))

    gdf_sck = gdf_sck.set_crs("EPSG:32613")

    #upload to db
    aqiGDL.log('Done with download')

    aqiGDL.gdf_to_db(gdf_sck, 'smartcitizen',
                        schema='public', if_exists='append')
    aqiGDL.log('Data in DB')
            


if __name__ == "__main__":
    aqiGDL.log('Starting script')
    main()