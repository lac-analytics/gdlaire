################################################################################
# Module: Analysis data
# updated: 08/10/2020
################################################################################

#from pathlib import Path
import json
import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from math import sqrt
import geopandas as gpd
import movingpandas as mpd
from datetime import datetime
import math



def interpolate_aq(pollutant, date, stations_aq, stations_MiMacro, interval='day', cellsize=0.01, hour='00'):
    """Function that creates a folium map with user specified city, pollutant and date and interpolates valid values


        Args:
            pollutant {str} -- pollutant to be plotted
            date {str} -- date to be analyzed in format yyyy-mm-dd, from 2014-01-01 to 2019-12-31.
            interval {str, optional} -- interval that will be added from start to end date, it can be day or hour. Defaults to 'day'.
            stations_aq {gdf} -- gdf with air quality stations
            stations_MiMacro {gdf} -- gdf with MiMacroPeriferico stations
            cell_size {float} -- cell size for the interpolation in degrees. Defaults to 0.01.
            hour {str} -- hour to interpolate in format hh from 00 to 23, only used when interval=hour. Defaults to 00.

        Returns:
            gdf -- gdf with interpolated concentration for the specified pollutant
    """

    dir_pcs = '../data/processed/'

    data_csv = dir_pcs+date[0:4]+'_'+interval+'.csv'

    data_bydateParam = pd.read_csv(data_csv).set_index('FECHA')
    data_bydateParam = data_bydateParam[data_bydateParam['PARAM'] == pollutant]

    # checks for interval and filters df
    if interval == 'hour':
        if int(hour) > 23 or int(hour) < 0:
            raise ValueError('Hour must be between 00 and 23')
        else:
            data_bydateParam = data_bydateParam[data_bydateParam['HORA']
                                                == hour+str(':00')]

    # lists to append valid values of lat and long for interpolation

    x = []
    y = []

    for i, est in stations_aq.iterrows():

        est_code = stations_aq.loc[(i), 'codigo']
        c_value = data_bydateParam.loc[(date), est_code]

        # appends coordinates from SIMAJ stations
        x.append(est.long)
        y.append(est.lat)

    # Registers the boundries coordinates of MiMacro Periferico stations
    min_x, min_y, max_x, max_y = stations_MiMacro.geometry.total_bounds

    # Checks for outer coordinates within air quality stations for the interpolation
    if min(x) < min_x:
        min_x = min(x)

    if max(x) > max_x:
        max_x = max(x)

    if min(y) < min_y:
        min_y = min(y)

    if max(y) > max_y:
        max_y = max(y)

    # Valor de potencia
    p = 2

    # x and y values for the start of the interpolation
    xidw = min_x
    yidw = min_y

    # Variables for interpolation
    dividendo = 0
    divisor = 0
    idw = []

    # interpolates the data
    while xidw <= max_x:
        while yidw <= max_y:
            for i, est in stations_aq.iterrows():

                est_code = stations_aq.loc[(i), 'codigo']
                c_value = data_bydateParam.loc[(date), est_code]

                if pd.notna(c_value):
                    dividendo = (
                        c_value/(sqrt((est.long-xidw)**2+(est.lat-yidw)**2)**(p))) + dividendo
                    divisor = (
                        1/(sqrt((est.long-xidw)**2+(est.lat-yidw)**2)**(p))) + divisor

            concentracion = dividendo/divisor

            idw.append([yidw, xidw, concentracion])
            yidw = yidw + cellsize
            dividendo = 0
            divisor = 0
        xidw = xidw + cellsize
        yidw = min_y

    # adds interpolated data to DataFrame
    inter = pd.DataFrame(idw, columns=['lat', 'long', 'conc'])

    # transforms DataFrame to GeoDataFrame
    inter_gdf = gpd.GeoDataFrame(
        inter, geometry=gpd.points_from_xy(inter.long, inter.lat))

    # sets crs
    inter_gdf.set_crs(epsg=4326, inplace=True)

    return(inter_gdf)


def interpolate_atpoint(long_int, lat_int, simaj, potencia=2):

    potencia = 2

    dividendo = 0

    divisor = 0

    for est in simaj.EST_SIMAJ.unique():

        lat_est = float(simaj.loc[simaj.EST_SIMAJ == est]['LAT'])
        long_est = float(simaj.loc[simaj.EST_SIMAJ == est]['LONG'])

        c_value = float(simaj.loc[simaj.EST_SIMAJ == est]['CONC'])

        if pd.notna(c_value):
            dividendo = (
                c_value/(sqrt((long_est-long_int)**2+(lat_est-lat_int)**2)**(potencia))) + dividendo
            divisor = (
                1/(sqrt((long_est-long_int)**2+(lat_est-lat_int)**2)**(potencia))) + divisor

    if divisor == 0:

        concentracion = -1

    else:
        concentracion = dividendo/divisor

    return (concentracion)


def moving_measure(df_mes, gdf):
    """ Function that interpolates positions into DataFrame based on GeoDataFrame time and position

    Args:
        df_mes {DataFrame} -- DataFrame with measurements by time from the PlumeLabs api
        gdf {GeoDataFrame} -- GeoDataFrame with positions by time from the PlumeLabs api

    Returns:
        DataFrame
    """

    for g in list(gdf.group.unique()):
    
        if len(gdf.loc[gdf.group==g]) >= 2:
            
            gdf_traj = gdf.loc[gdf.group==g].copy()
            
            df_mes_pos = df_mes.loc[(df_mes.date>=gdf_traj.date.min())&(df_mes.date<=gdf_traj.date.max())].copy()
            
            traj = mpd.Trajectory(gdf_traj, 1)
                    
            
            for i in range(0, len(df_mes_pos)):
                
                pos = (traj.interpolate_position_at(datetime(df_mes_pos.iloc[i]['datetime'].year,
                                                    df_mes_pos.iloc[i]['datetime'].month,
                                                    df_mes_pos.iloc[i]['datetime'].day,
                                                    df_mes_pos.iloc[i]['datetime'].hour,
                                                    df_mes_pos.iloc[i]['datetime'].minute,
                                                    df_mes_pos.iloc[i]['datetime'].second)))

                df_mes.loc[(df_mes.date==df_mes_pos.iloc[i]['date']),'latitude'] = pos.y
                df_mes.loc[(df_mes.date==df_mes_pos.iloc[i]['date']),'longitude'] = pos.x
                df_mes.loc[(df_mes.date==df_mes_pos.iloc[i]['date']),'trip_type'] = 'moving'
                df_mes.loc[(df_mes.date==df_mes_pos.iloc[i]['date']),'group'] = g

    return df_mes

def stationary_measure(df_mes, gdf):
    """ Function that adds positions into DataFrame based on the nearest position in GeoDataFrame

    Args:
        df_mes {DataFrame} -- DataFrame with measurements by time from the PlumeLabs api
        gdf {GeoDataFrame} -- GeoDataFrame with positions by time from the PlumeLabs api

    Returns:
        DataFrame
    """

    for i in range(len(df_mes)):
    
        traj = mpd.Trajectory(gdf,1)

        if 'longitude' in df_mes.columns:
        
            if math.isnan(df_mes.iloc[i]['longitude']):
                
                pos = (traj.get_position_at(datetime(int(df_mes.iloc[i]['datetime'].year),
                                                        int(df_mes.iloc[i]['datetime'].month),
                                                        int(df_mes.iloc[i]['datetime'].day),
                                                        int(df_mes.iloc[i]['datetime'].hour),
                                                        int(df_mes.iloc[i]['datetime'].minute),
                                                        int(df_mes.iloc[i]['datetime'].second)), method='nearest'))

                df_mes.loc[i,'latitude'] = pos.y
                df_mes.loc[i,'longitude'] = pos.x
                df_mes.loc[i,'trip_type'] = 'stationary'
                df_mes.loc[i,'group'] = 0

        else:
            try:
                pos = (traj.get_position_at(datetime(int(df_mes.iloc[i]['datetime'].year),
                                                            int(df_mes.iloc[i]['datetime'].month),
                                                            int(df_mes.iloc[i]['datetime'].day),
                                                            int(df_mes.iloc[i]['datetime'].hour),
                                                            int(df_mes.iloc[i]['datetime'].minute),
                                                            int(df_mes.iloc[i]['datetime'].second)), method='nearest'))

                df_mes.loc[i,'latitude'] = pos.y
                df_mes.loc[i,'longitude'] = pos.x
                df_mes.loc[i,'trip_type'] = 'stationary'
                df_mes.loc[i,'group'] = 0

            except:
                df_mes.loc[i,'latitude'] = np.nan
                df_mes.loc[i,'longitude'] = np.nan
                df_mes.loc[i,'trip_type'] = 'stationary'
                df_mes.loc[i,'group'] = 0


    return df_mes