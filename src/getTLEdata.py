import requests
from bs4 import BeautifulSoup as bs
import numpy as np

class GETTLE:

    """
    Class to retrieve 3LE data from space-track.org
    """

    def __init__(self, un, pw,
                 controller='basicspacedata',
                 actions='query',
                 classes='gp',
                 epoch_range='%3Enow-30',
                 order=None,
                 data_format='3le'):

        """
        Initializing parameters
        :param un: username for the space-track website -> str
        :param pw: password for the space-track website -> str
        :param controller: controller to request from space-track.org api
        :param actions: actions to request from space-track.org api
        :param classes: classes to request from space-track.org api
        :param epoch_range: the range of epoch to request data from space-track.org api
        :param order: sorting the data by the order for the data from space-track.org api
        :param data_format: the output format of the data from the space-track.org api
        """

        self.un = un
        self.pw = pw
        self.controller = controller
        self.actions = actions
        self.classes = classes
        self.epoch_range = epoch_range
        if order is None: self.order = ['NORAD_CAT_ID', 'EPOCH']
        self.data_format = data_format

    def request_data(self):
        """
        Main function which request data from space-track.org using the provided information
        :return: TLE data -> list['line1','line2', 'line3', ...]
        """

        # What is the login page

        url = 'https://www.space-track.org/'
        login_route = 'auth/login'

        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        # Get the HTML that we want

        with requests.session() as client:
            # Get csrftoken
            cookiejar = client.get(url + login_route).cookies
            cookies = cookiejar.get_dict(domain='www.space-track.org')
            cookie = cookies['spacetrack_csrf_cookie']

            # What you have to enter to login
            login_payload = {
                'spacetrack_csrf_token': cookie,
                'identity': self.un,
                'password': self.pw,
                'btnLogin': 'LOGIN'
            }

            # Post the data to login
            login_request = client.post(url + login_route, headers=HEADERS, data=login_payload)

            # Check if we are logged in or not
            assert login_request.status_code == 200, 'Not logged in.'
            cookies = login_request.cookies  # save the cookies for the login

            # Use beautiful soup to extract the HTML that we want
            # Configure the api query using the parameter inputs for this class
            combined_order = ','.join(self.order)
            api_query = ('https://www.space-track.org/' + str(self.controller) + '/' +
                         str(self.actions) + '/class/' + str(self.classes) + '/' +
                         'EPOCH/' + str(self.epoch_range) + '/orderby/' +
                         str(combined_order) + '/format/' + str(self.data_format))
            TLE_data_page = client.get(api_query)
            soup = bs(TLE_data_page.text, 'html.parser')

            TLE_data_1string = str(soup.text)

            # Split the long string by newlines and make it an array of strings
            TLE_data = TLE_data_1string.splitlines()

            return np.asarray(TLE_data, dtype=str)

# Test code
# get_tle = GETTLE(un='', pw='')
# TLE_data = get_tle.request_data()
# print(TLE_data)