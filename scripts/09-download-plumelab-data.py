import os
import sys
import geopandas as gpd
import pandas as pd
import numpy as np

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def main():

    sensor_id = [13164, 13335, 13954, 13920, 14835, 13178, 14002, 13116, 13684, 15602,
                 14823, 13597, 14811, 13593, 13703, 14829, 14204, 14834, 13093, 14618,
                 13595, 13638, 14709, 13949, 14616, 14794, 13360, 13946, 14669, 14700]

    gdf_all = gpd.GeoDataFrame()

    for s in sensor_id:
        s = str(s)
        ti = str(1590987600)
        tf = str(1612850399)
        register = 'measures', 'positions'

        url = (
            f'https://api.plumelabs.com/2.0/organizations/58/sensors/{register[0]}?token=pNogJHPUrTzuBFhElACiZkdV&sensor_id={s}&start_date={ti}&end_date={tf}')

        # Download data from the PlumeLabs api

        df_mes = aqiGDL.plume_data(url, register[0])

        if len(df_mes) == 2000:

            o = 1

            url = (
                f'https://api.plumelabs.com/2.0/organizations/58/sensors/{register[0]}?token=pNogJHPUrTzuBFhElACiZkdV&sensor_id={s}&start_date={ti}&end_date={tf}&offset={2000*o}')

            df_mes_t = aqiGDL.plume_data(url, register[0])

            df_mes = df_mes.append(df_mes_t)

            while len(df_mes_t) == 2000:

                o += 1

                url = (
                    f'https://api.plumelabs.com/2.0/organizations/58/sensors/{register[0]}?token=pNogJHPUrTzuBFhElACiZkdV&sensor_id={s}&start_date={ti}&end_date={tf}&offset={2000*o}')

                df_mes_t = aqiGDL.plume_data(url, register[0])

                df_mes = df_mes.append(df_mes_t)

        df_mes.reset_index(inplace=True)
        df_mes.drop(columns=['index'], inplace=True)

        aqiGDL.log(
            f'Downloaded a total of {len(df_mes)} for {register[0]} for {s}')

        url = (
            f'https://api.plumelabs.com/2.0/organizations/58/sensors/{register[1]}?token=pNogJHPUrTzuBFhElACiZkdV&sensor_id={s}&start_date={ti}&end_date={tf}')

        df_pos = aqiGDL.plume_data(url, register[1])

        if len(df_pos) == 2000:

            o = 1

            url = (
                f'https://api.plumelabs.com/2.0/organizations/58/sensors/{register[1]}?token=pNogJHPUrTzuBFhElACiZkdV&sensor_id={s}&start_date={ti}&end_date={tf}&offset={2000*o}')

            df_pos_t = aqiGDL.plume_data(url, register[1])

            df_pos = df_pos.append(df_pos_t)

            while len(df_pos_t) == 2000:

                o += 1

                url = (
                    f'https://api.plumelabs.com/2.0/organizations/58/sensors/{register[1]}?token=pNogJHPUrTzuBFhElACiZkdV&sensor_id={s}&start_date={ti}&end_date={tf}&offset={2000*o}')

                df_pos_t = aqiGDL.plume_data(url, register[1])

                df_pos = df_pos.append(df_pos_t)

        df_pos.reset_index(inplace=True)
        df_pos.drop(columns=['index'], inplace=True)

        aqiGDL.log(
            f'Downloaded a total of {len(df_pos)} for {register[1]} for {s}')

        if len(df_pos) > 0 and len(df_mes) > 0:

            # Create groups for trips

            df_pos = aqiGDL.time_break_trips(df_pos)

            # Passes positions DataFrame as a GeoDataFrame and prepares it for Moving Pandas

            gdf = gpd.GeoDataFrame(df_pos, geometry=gpd.points_from_xy(
                df_pos.longitude, df_pos.latitude))

            gdf.sort_values(by='date', inplace=True)
            gdf.reset_index(inplace=True)
            gdf.drop(columns=['index'], inplace=True)

            gdf = gdf.set_crs("EPSG:4326")
            gdf = gdf.to_crs("EPSG:32613")

            gdf.longitude = gdf.geometry.x
            gdf.latitude = gdf.geometry.y

            gdf['type'] = 'moving'

            gdf['datetime'] = pd.to_datetime(gdf['date'],
                                             errors='coerce', unit='s')
            gdf.set_index('datetime', inplace=True)

            # Prepares measurements DataFrame before interpolating positions with Moving Pandas

            df_mes.sort_values(by='date', inplace=True)
            df_mes.reset_index(inplace=True)
            df_mes.drop(columns=['index'], inplace=True)

            df_mes['datetime'] = pd.to_datetime(df_mes['date'],
                                                errors='coerce', unit='s')

            df_mes = aqiGDL.moving_measure(df_mes, gdf)

            aqiGDL.log(
                f'Interpolated position data for moving measurements for {s}')

            df_mes = aqiGDL.stationary_measure(df_mes, gdf)

            aqiGDL.log(
                f'Interpolated position data for stationary measurements for {s}')

            # Merge GeoDataFrames
            df_merge = pd.merge(df_mes, gdf, how='outer')
            df_merge.sort_values(by='date', inplace=True)
            df_merge.reset_index(inplace=True)
            df_merge.drop(
                columns=['index', 'horizontal_accuracy', 'diff', 'geometry'], inplace=True)

            # Change timezones
            df_merge['datetime'] = pd.to_datetime(
                df_merge['date'], errors='coerce', unit='s')
            df_merge['datetime'] = df_merge['datetime'].dt.tz_localize(
                "GMT").dt.tz_convert('America/Mexico_City').dt.tz_localize(None)

            aqiGDL.log(f'Changed timezone for {s}')

            # Interpolate measures into positions
            gdf_mes = gpd.GeoDataFrame(df_mes, geometry=gpd.points_from_xy(
                df_mes.longitude, df_mes.latitude))
            gdf_mes = gdf_mes.set_crs("EPSG:32613")

            df_merge.interpolate(
                method='linear', limit_direction='forward', axis=0, inplace=True)
            df_merge.dropna(inplace=True)

            aqiGDL.log(
                f'Interpolated air quality data for position measurements for {s}')

            # Max Pollution Index
            gdf_aq = gpd.GeoDataFrame(df_merge, geometry=gpd.points_from_xy(
                df_merge.longitude, df_merge.latitude))

            gdf_aq = gdf_aq.set_crs("EPSG:32613")

            gdf_aq.set_index('datetime', inplace=True)

            gdf_aq['pi'] = gdf_aq[['pollutants.no2.pi', 'pollutants.voc.pi',
                                   'pollutants.pm25.pi', 'pollutants.pm10.pi', 'pollutants.pm1.pi']].max(axis=1)

            gdf_aq['sensor_id'] = s

            gdf_all = gdf_all.append(gdf_aq)
            aqiGDL.log('Done with download')
            aqiGDL.gdf_to_db(gdf_all, 'plumbe', if_exists='append')
            aqiGDL.log('Data in DB')


if __name__ == "__main__":
    main()
