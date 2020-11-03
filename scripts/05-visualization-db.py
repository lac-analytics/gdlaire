import os
import sys
import geopandas as gpd
import pandas as pd

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def main(pollutant, date, interval, hour='00', save=False):

    stations_MiMacro = gpd.read_file(
        '../data/external/estaciones_MiMacroPeriferico.geojson')

    aqiGDL.log('MiMacroPeriferico stations loaded')

    stations_pd = pd.read_csv('../data/raw/estaciones.csv')

    aqiGDL.log('Air quality stations loaded')

    stations_aq = gpd.GeoDataFrame(
        stations_pd, geometry=gpd.points_from_xy(stations_pd.long, stations_pd.lat))

    aqiGDL.log('Air quality stations to gdf')

    s = aqiGDL.interpolate_aq(pollutant, date, stations_aq,
                              stations_MiMacro, interval=interval, cellsize=0.005, hour=hour)

    if interval == 'day':
        aqiGDL.log(
            f'Air quality interpolation created for Pollutant: {pollutant} Date: {date} Interval: {interval}')
    else:
        aqiGDL.log(
            f'Air quality interpolation created for Pollutant: {pollutant} Date: {date} Interval: {interval} Hour: {hour}')

    s_vis = aqiGDL.symbology_gdf(s, pollutant)

    if save:
        if interval == 'hour':
            time = hour+'h_'+interval
        else:
            time = interval

        # removes - to avoid syntax error in db
        date_db = date.replace('-', '')

        aqiGDL.gdf_to_db(s_vis, pollutant+'_'+date_db+'_'+time,
                         schema='interpolation', if_exists='replace')  # uploads to db


if __name__ == "__main__":

    sets = ['hour', 'day']
    pollutants = ['PM10', 'O3', 'SO2', 'NO2', 'CO']
    start_date = ['2019-01-']

    for p in pollutants:

        for d in range(1, 32, 1):

            d_time = '{:02d}'.format(d)

            for s in sets:

                if s == 'hour':

                    for h in range(24):
                        h_time = '{:02d}'.format(h)
                        main(p, start_date[0]+str(d_time),
                             s, save=True, hour=h_time)

                else:
                    main(p, start_date[0]+str(d_time), s, save=True)
