"""
 ___________   _________     _____________   ______________    ______            ______
|     ______| |   ___   >\  |_____   _____| |_____    _____|  /< __ >\          /> __ <\
|    |______  |  |   \   >\      |   |           |    |      /> |__| <\        /< |__| >\
|_______    | |  |    |  >|      |   |           |    |     /< ______ >\      /> ______ <\
 ______|    | |  |___/   >/  ____|   |____       |    |    /> |      | <\    /< |      | >\
|___________| |_________>/  |_____________|      |____|   /<__|      |__>\  />__|      |__<\

"""
from sgp4.api import jday, Satrec, SatrecArray
import numpy as np
import pandas as pd
import os
import json
import datetime
from typing import List, Tuple
from dateutil.parser import parse
from nptyping import NDArray


class SGP4PREDICT:
    """
    Class to predict the space debris trajectory using the sgp4 algorithm for a specified date
    """

    def __init__(self, tledata: List[str] = None,
                 linespertle=3,
                 start_date: str = str(datetime.datetime.utcnow()),
                 end_date: str = None,
                 interval: str = "D") -> None:
        """
        Initialize parameters for class (timezone is UTC Gregorian)
        :param tledata: the TLE data input
        :param linespertle: 2 line or 3 line data :: int (2 or 3)
        :param start_date: the start date to instigate prediction :: YYYY-MM-DD HH:MM:SS
        -> Year: 4 digits, Month: 01-12, Day: 01-31, Hour: 01-24, Minute: 01-60, Second: 01-60
        :param end_date: the end date to terminate prediction :: YYYY-MM-DD HH:MM:SS
        -> Year: 4 digits, Month: 01-12, Day: 01-31, Hour: 01-24, Minute: 01-60, Second: 01-60
        :param interval: The interval to get the data, string D: days; W: weeks; M: months; Y: years; H: hours;
                         T: minutes; S: seconds; L: miliseconds; U: microseconds; N: nanoseconds
                         combining it with a number allows to change the interval e.g. 2D: 2 days
        """

        self.tledata = tledata
        self.linespertle = linespertle
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self._dates = None
        self._position = None
        self._velocity = None

    def get_dates(self) -> List[str]:
        """
        Function that gets dates based on start date, end date, and interval
        :return: the array of dates
        """

        tspan = pd.date_range(start=self.start_date, end=self.end_date, freq=self.interval)
        temp_df = pd.DataFrame(tspan)
        temp_df = temp_df.astype(str)
        temp = temp_df.values.tolist()
        time_list = np.reshape(temp, (1, np.shape(temp)[0]))[0].tolist()
        assert isinstance(time_list, object), "Is not object"
        return time_list

    @staticmethod
    def convert2JulianDate(date_list: List[str]) -> Tuple[NDArray, NDArray]:
        """
        Function that creates a list of Julian Dates and decimals from the UTC date list
        :param date_list: the list of dates: List[str]
        :return: the list of Julian Dates and fr
        """

        dates = [parse(dt) for dt in date_list]
        jd, fr = [], []
        for d in dates:
            jd_temp, fr_temp = jday(d.year, d.month, d.day, d.hour, d.minute, d.second)
            jd.append(jd_temp)
            fr.append(fr_temp)
        # Convert to numpy array
        jd = np.array(jd)
        fr = np.array(fr)
        return jd, fr

    def config_sats(self):
        """
        Function that configures the satellites into a SatrecArray object
        :return: SatrecArray object
        """

        # Loop through the TLE data to create a SatrecArray with several individual space objects
        satellites = []  # SatrecArray to store all space objects

        if self.linespertle == 2:
            m = 0
        else:
            m = 1

        for i in range(0, len(self.tledata), self.linespertle):
            line1 = self.tledata[i + m]
            line2 = self.tledata[i + (m + 1)]

            # Check to see if the Elset Classification is 'U' indicating that it is an
            # unclassified object, that is, a space debris
            if self.tledata[i + m].split()[1][-1] == 'U':
                satellites.append(Satrec.twoline2rv(line1, line2))

        sats = SatrecArray(satellites)
        return sats

    def run_sgp4(self) -> Tuple[NDArray, NDArray]:
        """
        Function that performs the sgp4 prediction
        :return: numpy arrays of positition vectors and velocity vectors in TEME coordinates
        """

        dates = self.get_dates()
        self._dates = dates
        julian_days, fractions = self.convert2JulianDate(dates)
        sat_objects = self.config_sats()
        err, r, v = sat_objects.sgp4(jd=julian_days, fr=fractions)
        self._position = r
        self._velocity = v
        return r, v

    def export_json(self) -> None:
        """
        Function that exports data to json file
        :return: none
        """

        res_dict = {'Dates': self._dates,
                    'Postion in TEME (km)': self._position.tolist(),
                    'Velocity in TEME (km/s)': self._velocity.tolist()}

        while True:
            file_name = input('Name your JSON file -> ')
            if ".json" not in file_name:
                print("Add the .json extension on your file name.")
            else:
                break
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, 'w') as jfile:
            json.dump(res_dict, jfile, indent=4)


def main():
    TLE_sample = ['0 VANGUARD 1',
                  '1     5U 58002B   20270.72609959 +.00000008 +00000-0 +35143-4 0  9996',
                  '2     5 034.2447 276.2975 1845776 088.0693 292.9082 10.84868479216254',
                  '0 VANGUARD 2',
                  '1    11U 59001A   20270.83057634 -.00000014 +00000-0 -52792-5 0  9991',
                  '2    11 032.8687 034.7609 1467087 103.7620 273.0083 11.85679410287012',
                  '0 VANGUARD R/B',
                  '1    12U 59001B   20270.89554473 +.00000372 +00000-0 +19820-3 0  9999',
                  '2    12 032.9137 356.0609 1666130 249.2921 092.1676 11.44320987291609',
                  '0 VANGUARD R/B',
                  '1    16U 58002A   20270.85942587 -.00000022 +00000-0 -46274-4 0  9994',
                  '2    16 034.2702 221.8316 2022572 305.2573 037.4791 10.48675665469485',
                  '0 VANGUARD 3',
                  '1    20U 59007A   20270.48712837 +.00000328 +00000-0 +14121-3 0  9999',
                  '2    20 033.3411 182.1436 1666591 082.6853 295.9308 11.55733657242298',
                  '0 EXPLORER 7',
                  '1    22U 59009A   20270.68850821 +.00000323 +00000-0 +46901-4 0  9998',
                  '2    22 050.2861 347.0443 0139436 285.4847 073.0739 14.95205750485528',
                  '0 TIROS 1',
                  '1    29U 60002B   20270.51303602 -.00000101 +00000-0 +16003-4 0  9997',
                  '2    29 048.3794 191.6811 0024581 304.4255 055.4334 14.74372853233453',
                  '0 TRANSIT 2A',
                  '1    45U 60007A   20270.87697544 -.00000081 +00000-0 +70910-5 0  9995',
                  '2    45 066.6929 113.6127 0262116 242.5192 114.9042 14.33687614080375',
                  '0 SOLRAD 1 (GREB)',
                  '1    46U 60007B   20270.90681461 +.00000039 +00000-0 +31064-4 0  9999',
                  '2    46 066.6896 132.4066 0203897 054.4060 307.5857 14.49317409153818',
                  '0 THOR ABLESTAR R/B',
                  '1    47U 60007C   20270.67888321 -.00000040 +00000-0 +16368-4 0  9991',
                  '2    47 066.6644 244.3196 0233780 230.3761 127.6505 14.42103295149279',
                  '0 DELTA 1 R/B',
                  '1    50U 60009B   20270.45814876 -.00000089  00000-0 -40244-4 0  9991',
                  '2    50  47.2307 167.7862 0113683 266.9466  91.8310 12.20112284683000',
                  '0 ECHO 1 DEB (METAL OBJ)',
                  '1    51U 60009C   20270.77783235 -.00000155 +00000-0 -66528-3 0  9997',
                  '2    51 047.2148 033.9443 0107347 105.2138 256.0549 12.18276304676444',
                  '0 COSMOS 86',
                  '1  1584U 65073A   20270.84441890 -.00000096 +00000-0 -90198-6 0  9998',
                  '2  1584 056.0607 043.0461 0211763 335.4680 193.5629 12.51876101515807', ]

    # Add custom date to conduct prediction
    ti = "2020-10-11 00:02:30"
    tf = "2020-12-12 14:02:30"
    sgp4sim = SGP4PREDICT(tledata=TLE_sample, linespertle=3, start_date=ti, end_date=tf, interval="D")
    r, v = sgp4sim.run_sgp4()
    # sgp4sim.export_json() # test to see if data can be retrieved properly

if __name__ == '__main__': main()
