from enum import Enum
from os import mkdir
from requests import post
from os.path import exists
import pandas as pd
from imdlib import open_data
from dataclasses import dataclass

class WeatherDataType(Enum):
    RAIN = 1
    MAXTEMP = 2
    MINTEMP = 3

@dataclass
class Location:
    logitude : float
    lattitude : float

def get_data(var_type, start_yr, end_yr=None, fn_format=None, file_dir=None, sub_dir=False, proxies=None):
    
    if var_type == 'rain':
        var = 'rain'
        url = 'https://imdpune.gov.in/Clim_Pred_LRF_New/rainfall.php'
        fini = 'Rainfall_ind'
        if fn_format == 'yearwise':
            fend = '.grd'
        else:
            fend = '_rfp25.grd'
    elif var_type == 'tmax':
        var = 'maxtemp'
        url = 'https://imdpune.gov.in/Clim_Pred_LRF_New/maxtemp.php'
        fini = 'Maxtemp_MaxT_'
        fend = '.GRD'
    elif var_type == 'tmin':
        var = 'mintemp'
        url = 'https://imdpune.gov.in/Clim_Pred_LRF_New/mintemp.php'
        fini = 'Mintemp_MinT_'
        fend = '.GRD'
    else:
        raise Exception("Error in variable type declaration."
                        "It must be 'rain'/'tmin'/'tmax'. ")

    # Handling ending year not given case
    if sum([bool(start_yr), bool(end_yr)]) == 1:
        end_yr = start_yr

    # years = np.arange(start_yr, end_yr + 1)



    for year in [2020]:
        # Setting parameters
        print("Downloading: " + var + " for year " + str(year))

        data = {var: year}
        # Requesting the dataset
        response = post(url, data=data, proxies=proxies)
        response.raise_for_status()
        print(url)
        print(data)

        # Saving file
        with open('tmin/xyz.grd', 'wb') as f:
            f.write(response.content)

    print("Download Successful !!!")

    data = open_data(var_type, start_yr, end_yr, fn_format, file_dir)
    return data


def __save_gridded_data(year : int, d_type : WeatherDataType):
    d_type_name = WeatherDataType(d_type).name.lower()
    post_url : str = 'https://www.imdpune.gov.in/Clim_Pred_LRF_New/'
    post_data : dict = dict()
    dest_file_path : str = None
    if d_type == WeatherDataType.RAIN:
        post_url += 'rainfall.php'
        post_data['rain'] = year
        dest_file_path = f'rain{year}.GRD'
    elif d_type == WeatherDataType.MAXTEMP:
        post_url += f'{d_type_name}.php'
        post_data[d_type_name] = year
        dest_file_path = f'tmax{year}.GRD'
    elif WeatherDataType.MINTEMP:
        post_url += f'{d_type_name}.php'
        post_data[d_type_name] = year
        dest_file_path = f'tmin{year}.GRD'
    else:
        raise Exception(f'Invalid Weather type {d_type_name} - It must be {WeatherDataType(WeatherDataType.MINTEMP).name.lower()}')

    if not exists(dest_file_path):
        if not exists(d_type_name.upper()):
            mkdir(d_type_name.upper())
        response = post(url=post_url, data=post_data)
        print(post_url)
        print(post_data)
        response.raise_for_status()
        with open(dest_file_path, 'wb') as f:
            f.write(response.content)

def __save_gridded_data_to_csv(year : int, d_type : WeatherDataType, location : Location):
    d_type_name = WeatherDataType(d_type).name.lower()
    data = open_data(d_type_name, year, year,'yearwise')
    data.to_csv('test.tmp', location.lattitude, location.logitude, '.')
    print(0)

def get_weather_by_type(d_type : WeatherDataType, years : list, location : Location):
    for year in years:
        # get_data('tmax', 2020, 2020)
        __save_gridded_data(year, d_type=d_type)
        __save_gridded_data_to_csv(year, d_type=d_type, location=location)


if __name__ == '__main__':
    get_weather_by_type(WeatherDataType.MAXTEMP, years=[2020], location=Location(21.03, 77.23))