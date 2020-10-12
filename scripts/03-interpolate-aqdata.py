# Create geojson with interpolation

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
                              stations_MiMacro, interval=interval, cellsize=0.01, hour=hour)

    if interval =='day':
        aqiGDL.log(
            f'Air quality interpolation created for Pollutant: {pollutant} Date: {date} Interval: {interval}')
    else:
        aqiGDL.log(
            f'Air quality interpolation created for Pollutant: {pollutant} Date: {date} Interval: {interval} Hour: {hour}')

    if save:
        if interval=='hour':
            time = hour+'h_'+interval
        else:
            time = interval

        s.to_file(r''+'../data/processed/'+pollutant+'_'+date+'_'+time +
                  '.geojson', driver='GeoJSON', index=False, header=True)  # saves to csv


if __name__ == "__main__":
    main('PM10', '2018-12-20', 'hour', save=True, hour='23')
