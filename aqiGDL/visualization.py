################################################################################
# Module: Visualization of data
# updated: 31/10/2020
################################################################################

import geopandas as gpd
import os
from math import sqrt


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import textwrap

import numpy as np



def p_limits(param):
    """Function that returns a limit value for a bad air quality

    Args:
        param {str} -- str with criteron pollutant chemical formula

    Returns:
        int -- int with limit value
    """

    limit_dict = {'PM10': 214, 'O3': 0.154, 'CO': 16.5,
                  'PM25': 97.4, 'SO2': 0.195, 'NO2': 0.315}

    return (limit_dict[param])


def imeca_colours(param, conc):
    """Function that takes a pollutant and concentration, calculates its IMECA and returns a hex,
        IMECA calculation based on: https://rama.edomex.gob.mx/imeca

    Args:
        param {str} -- str with criteron pollutant chemical formula
        conc {float} -- concentration for the pollutant

    Returns:
        str -- sr with the hex code
    """

    imeca = 0

    if param == 'CO':

        imeca = conc * 100 / 11

    elif param == 'SO2':

        imeca = (conc/1000) * 100 / 0.11

    elif param == 'NO2':

        imeca = (conc/1000) * 100 / 0.21

    elif param == 'O3':

        conc = conc/1000

        if conc <= 0.07:
            imeca = 714.29*conc

        elif 0.07 < conc <= 0.095:
            imeca = 2041.67*(conc-0.071)+51

        elif 0.095 < conc <= 0.154:
            imeca = 844.83*(conc-0.096)+101

        elif 0.154 < conc <= 0.204:
            imeca = 1000*(conc-0.155)+151

        elif 0.204 < conc <= 0.404:
            imeca = 497.49*(conc-0.205)+201

        elif 0.404 < conc:
            imeca = 1000*(conc-104)

    elif param == 'PM10':

        if conc <= 40:
            imeca = 1.25*conc

        elif 40 < conc <= 75:
            imeca = 1.44*(conc-41)+51

        elif 75 < conc <= 214:
            imeca = 0.355*(conc-76)+101

        elif 214 < conc <= 354:
            imeca = 0.353*(conc-215)+151

        elif 354 < conc <= 424:
            imeca = 1.4359*(conc-355)+201

        elif 424 < conc <= 504:
            imeca = 1.253*(conc-425)+301

        elif 504 < conc:
            imeca = conc-104

    if imeca <= 50:
        color = '#75b46f'

    elif 50 < imeca <= 100:
        color = '#f7ff55'

    elif 100 < imeca <= 150:
        color = '#ff9e4f'

    elif 150 < imeca <= 200:
        color = '#db3331'

    elif 200 < imeca:
        color = '#c158b8'

    else:
        color = '#ffffff'

    return (color)


def symbology_gdf(gdf, param):
    """Function that takes a geodataframe with points and concenrtations and returns
        that geodataframe with added columns for colours and sizes for each point

    Args:
        gdf {gdf} -- gdf with interpolated points with concentration for each point
        param {str} -- str with criteron pollutant chemical formula

    Returns:
        gdf -- gdf with added columns for hex colours and size according to concentration
    """

    for i in range(len(gdf)):

        #Selects concentration from gdf
        c_value = gdf.loc[gdf.index == i, 'conc'].values

        #Sets size according to limit
        c_symbol = 5*(c_value)/p_limits(param)

        #Sets colour according to concentration
        c_colour = imeca_colours(param, c_value)

        gdf.loc[gdf.index == i, 'Colour'] = c_colour
        gdf.loc[gdf.index == i, 'Size'] = c_symbol

    return gdf


def graph_smartcitizen(device, param, gdf, gdf_est, edges, save=False):

    fig, axes = plt.subplots(1,2,figsize=(24,8), sharex=True)

    df_temp = gdf[(gdf['device_id']==device) & (gdf['param']==param)].copy()
    df_temp['date'] = pd.to_datetime(df_temp['date'])
    df_temp.set_index('date',inplace=True)
    df_temp = df_temp.resample('D').mean()
    axes[1].scatter(df_temp.index, df_temp['value'], label=param)

    title = textwrap.fill(param, 35)
    axes[1].set_title(title,fontsize=20)
    axes[1].tick_params(axis='x',labelrotation=45)


    x_ticks = np.arange(0, len(df_temp.index),15)

    a00 = axes[0]
    shax = a00.get_shared_x_axes()
    shax.remove(a00)
    edges.plot(ax=axes[0], color='#e8e9eb',linewidth=0.1, zorder=-1)
    edges[(edges['highway']=='primary') | (edges['highway']=='secondary')].plot(ax=axes[0], color='#e8e9eb',linewidth=0.5, zorder=0)
    gdf_est.plot(ax=axes[0], color='k', alpha=0.85, zorder=1)
    gdf_est[gdf_est.index==device].plot(ax=axes[0], color='#ba0d38', alpha=0.85, zorder=2, markersize=90)
    axes[0].axis('off')
    estacion = device
    fecha_1 = df_temp.index.min().strftime("%Y-%m-%d")
    fecha_2 = df_temp.index.max().strftime("%Y-%m-%d")
    fig.suptitle(f'Device: {estacion}\n{fecha_1} -- {fecha_2}', fontsize=30)

    if save==True:
        plt.savefig(f'{device}_{fecha_1}_{fecha_2}.png',dpi=300)

    return plt.show()