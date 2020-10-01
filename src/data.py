################################################################################
# Module: Data gathering and treatment
# updated: 01/10/2020
################################################################################

from pathlib import Path
import os
import osmnx as ox
import pandas as pd
import numpy as np
import xlrd
import urllib.request
import math
from . import utils

from datetime import datetime, timedelta


def daterange(start_date, end_date, interval='hour', lapse=1):
    """Function that creates a list with dates from start to end according to interval.

    Args:
        start_date (datetime): start datetime value in format yyyy-mm-dd hh:mm.
        end_date (datetime): end datetime value in format yyyy-mm-dd hh:mm.
        interval (str, optional): interval that will be added from start to end date, it can be day or hour. Defaults to 'hour'.
        lapse (int, optional): time lapse increment. Defaults to 1.

    Returns:
        list: list of dates from start_date to end_date according to interval and lapse.
    """

    if interval == 'hour':
        delta = timedelta(hours=lapse)
    elif interval == 'day':
        delta = timedelta(days=lapse)

    date_list = []
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += delta

    return date_list


def simaj_download(year_start=2014, year_end=2019):
    """Function that downloads data from the SIMAJ database

    Args:
        year_start (int, optional): starting year to download. Defaults to 2014.
        year_end (int, optional): end year to download. Defaults to 2019.
    """

    for year in range(year_end-year_start+1):

        save_path = os.path.join(
            '../gdl-aire/gdlaire/data/raw/', 'datos_'+str(year_start+year)+'.xlsx')

        urllib.request.urlretrieve(
            'http://siga.jalisco.gob.mx/aire/reportes/datos_'+str(year_start+year)+'.xlsx', save_path)


def database_clean(interval='hour'):
    """Function that creates a new and clean database in .csv format from SIMAJ air quality database for the years 2014 to 2019.

    Args:
        interval (str, optional): it sets the interval for the new database, it can take 'hour' or 'day'. Defaults to 'hour'.
    """

    dir_gdl = '../gdl-aire/gdlaire/data/raw/'

    # dictionary for stations codes and names
    est_dict = {'ÁGUILAS': 'AGU', 'AGUILAS': 'AGU', 'LAS ÁGUILAS': 'AGU', 'ATEMAJAC': 'ATM', 'CENTRO': 'CEN',
                'LAS PINTAS': 'PIN', 'LOMA DORADA': 'LDO', 'MIRAVALLE': 'MIR', 'OBLATOS': 'OBL',
                'SANTA FE': 'SFE', 'SANTA FÉ': 'SFE', 'TLAQUEPAQUE': 'TLA', 'VALLARTA': 'VAL'}

    # check for file or directory in dir_gdl
    for file in os.listdir(dir_gdl):

        if file.endswith('.xlsx'):
            # SIMAJ data is in xls and in different sheets
            xls = xlrd.open_workbook(r''+dir_gdl+file, on_demand=True)
            sheets = xls.sheet_names()  # creates list form sheet names

        else:
            continue

        year = file[6:10]  # gathers the year from the file name

        start_date = datetime(int(year), 1, 1, 00, 00)  # start date for array
        end_date = datetime(int(year), 12, 31, 23, 00)  # end date for array

        # creates array for every hour of a given year
        date_array = np.array(
            daterange(start_date, end_date, interval=interval))

        # creates new df in which air quality data for all stations will be saved
        df = pd.DataFrame(index=np.array(range(0, len(date_array))), columns=[
                          'FECHA', 'HORA', 'O3', 'PM10', 'CO', 'NO2', 'SO2'])

        # datetime id counter
        dt_id = 0

        # saves date and hour data to df
        for t in date_array:
            df['FECHA'].iloc[dt_id] = t.date()
            df['HORA'].iloc[dt_id] = '{:02d}:{:02d}'.format(t.hour, t.minute)
            dt_id += 1

        # sets index before stack
        df = df.set_index(['FECHA', 'HORA'])

        # stacks DataFrame so for every date there are 5 rows with criterion pollutants
        df = df.stack(dropna=False)
        df = df.reset_index().rename(columns={'level_2': 'PARAM'})

        # sets index depending on interval type
        if interval == 'hour':
            df = df.set_index(['FECHA', 'HORA', 'PARAM'])
        else:
            df = df.set_index(['FECHA', 'PARAM']).drop(columns='HORA')

        for s in sheets:

            # reads excel with data and sets empty cells as nan
            gdl_data = pd.read_excel(
                dir_gdl+file, sheet_name=s).replace(r'^\s*$', np.nan, regex=True)

            gdl_data.rename(
                columns={gdl_data.columns[0]: 'FECHA', gdl_data.columns[1]: 'HORA'}, inplace=True)

            # fixes column names
            if int(year) == 2014 and s == 'Las Pintas':
                gdl_data.rename(
                    columns={gdl_data.columns[6]: 'SO2'}, inplace=True)

            if int(year) == 2018 and s != 'Vallarta':
                gdl_data.rename(
                    columns={gdl_data.columns[2]: 'O3'}, inplace=True)

            # fixes date
            if int(year) == 2018 and s == 'Centro':
                gdl_data['FECHA'].iloc[4112] = datetime.strptime(
                    '2018-06-21', '%Y-%m-%d')

            gdl_data.columns = gdl_data.columns.str.replace(
                ' ', '')  # removes spaces from columns

            # removes : from columns
            gdl_data.columns = [col.replace(':', '')
                                for col in gdl_data.columns]

            gdl_data = gdl_data[['FECHA', 'HORA', 'O3',
                                 'NO2', 'SO2', 'PM10', 'CO']]  # filters data

            # sets FECHA column as date
            gdl_data['FECHA'] = gdl_data['FECHA'].dt.date

            # iterates over hour data and gives it the appropiate format
            for i in range(len(gdl_data)):

                try:
                    # tries to set hour in hh:mm format according to HORA column
                    gdl_data['HORA'].iloc[i] = '{:02d}:{:02d}'.format(
                        gdl_data['HORA'].iloc[i].hour, gdl_data['HORA'].iloc[i].minute)

                except:

                    # nested tries
                    try:
                        # if HORA is float or int it gives it datetime format
                        time_type = gdl_data['HORA'].iloc[i]
                        seconds = (time_type - 25569) * 86400.0
                        time_datetime = datetime.utcfromtimestamp(seconds)

                        gdl_data['HORA'].iloc[i] = '{:02d}:{:02d}'.format(
                            time_datetime.hour, time_datetime.minute)

                    except:

                        # if HORA is nan it takes previous date and hour and adds +1h and stores it in date and time
                        prev_date = gdl_data['FECHA'].iloc[i-1]
                        prev_hour = gdl_data['HORA'].iloc[i-1]

                        prev_datetime = str(prev_date)+' '+str(prev_hour)

                        date_datetime = datetime.strptime(
                            prev_datetime, '%Y-%m-%d %H:%M')

                        new_datetime = date_datetime + timedelta(hours=1)

                        gdl_data['FECHA'].iloc[i] = new_datetime.date()
                        gdl_data['HORA'].iloc[i] = '{:02d}:{:02d}'.format(
                            new_datetime.hour, new_datetime.minute)

            # stacks gdl DataFrame so for every date there are 5 rows with criterion pollutants
            gdl_stack = pd.DataFrame(gdl_data.set_index(
                ['FECHA', 'HORA']).stack([0], dropna=False))

            # changes name from stacked column with concentration information
            gdl_stack = gdl_stack.reset_index().rename(columns={'level_2': 'PARAM',
                                                                0: est_dict[s.strip(' ').upper()]})

            gdl_stack['FECHA'] = pd.to_datetime(gdl_stack['FECHA'])

            # because the data base contains dates out from the analyzed year the DataFrame is filtered
            gdl_stack = gdl_stack[gdl_stack['FECHA'].dt.year == int(
                file[6:10])]

            # removes sapces from sheet names and sets columns as numbers avoiding spaces
            gdl_stack[est_dict[s.strip(' ').upper()]] = pd.to_numeric(
                gdl_stack[est_dict[s.strip(' ').upper()]], errors='coerce')

            if interval == 'day':
                gdl_stack = gdl_stack.drop(columns=['HORA'])
                gdl_stack = gdl_stack.groupby(['FECHA', 'PARAM']).mean()
            else:
                # it groups data to avoid doble dates in air quality database
                gdl_stack = gdl_stack.groupby(
                    ['FECHA', 'HORA', 'PARAM']).mean()

            # adds data from gdl_stack for a specified year to all_data which
            # will contain information for every year
            df = pd.merge(df, gdl_stack, how='left',
                          left_index=True, right_index=True)

        # drops coloumn 0 which is created when stacking df
        df = df.drop(columns=0)
        # saves data for all years, stations and parameters
        df.to_csv('../gdl-aire/gdlaire/data/processed/' +
                  file[6:10]+'_'+interval+'.csv')


def download_graph(polygon, city, network_type='walk'):
    """Download a graph from a bounding box, and saves it to disk

    Arguments:
            polygon {polygon} -- polygon to use as boundary to download the network
            city {str} -- string with the name of the city

    Keyword Arguments:
            network_type {str} -- String with the type of network to download (drive, walk, bike, all_private, all) for more details see OSMnx documentation

    Returns:
            nx.MultiDiGraph
    """
    utils.log("Downloading graph")
    G = ox.graph_from_polygon(polygon, network_type=network_type,
                              simplify=True, retain_all=False, truncate_by_edge=False)
    utils.log('Graph downloaded')
    return G
