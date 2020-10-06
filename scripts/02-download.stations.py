# Download csv to disk

import os
import sys

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    import aqiGDL


def main(save=False):

    aqiGDL.log('Call SINAICA')

    s = aqiGDL.sinaica_stations_csv()
    
    if save:
        s.to_csv (r''+'../data/raw/estaciones.csv', index = False, header=True) #saves to csv


if __name__ == "__main__":
    main(save=True)
