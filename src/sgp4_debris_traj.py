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

    def __init__(self, tledata: List[str]=None,
                 linespertle=3,
                 start_date: str=str(datetime.datetime.utcnow()),
                 end_date: str=None,
                 interval: str="D") -> None:
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

    @ staticmethod
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
            line2 = self.tledata[i + (m+1)]

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
