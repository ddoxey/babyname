import os
import re
import pickle
import hashlib
from bs4 import BeautifulSoup
from requests_cache import CachedSession

SSA_URL = 'https://www.ssa.gov/cgi-bin/babyname.cgi'

CACHE_PATH = os.path.join(os.environ["HOME"], '.babyname')


class BabyName:

    session = None


    def __init__(self):
        self.session = CachedSession(CACHE_PATH)


    @classmethod
    def _cache_filename_(cls, parameters):
        if 'HOME' not in os.environ:
            return None
        cache_dir = os.path.join(os.environ['HOME'], '.babyname-lookup')
        if not os.path.isdir(cache_dir):
            os.mkdir(cache_dir)
        m = hashlib.sha256()
        m.update(parameters['name'].lower().encode('utf8'))
        if parameters.get('start') is not None:
            m.update(parameters['start'].encode('utf8'))
        if parameters.get('sex') is not None:
            m.update(parameters['sex'].encode('utf8'))
        cache_key = m.hexdigest()
        return os.path.join(cache_dir, f'{cache_key}.pkl')


    @classmethod
    def _cache_get_(cls, parameters):
        filename = cls._cache_filename_(parameters)
        if os.path.exists(filename):
            with open(filename, 'rb') as pkl_fh:
                return pickle.load(pkl_fh)
        return None


    @classmethod
    def _cache_store_(cls, parameters, data):
        filename = cls._cache_filename_(parameters)
        with open(filename, 'wb') as pkl_fh:
            pickle.dump(data, pkl_fh)


    def lookup(self, name, start=1900, sex=None):

        parameters = {'name': name, 'start': str(start)}

        if sex is not None:
            if sex.lower() not in ['male', 'female', 'm', 'f']:
                raise Exception('sex must be either "male" or "female"')
            parameters['sex'] = sex[0].upper()

        if parameters['name'] is None:
            raise Exception("'name' is a required parameter")

        if not parameters['start'].isnumeric():
            raise Exception('start must be a year value >= 1900')

        data = self._cache_get_(parameters)

        if data is None:

            response = self.session.post(url=SSA_URL, data=parameters)

            if not response.ok:
                return None

            content = response.content.decode('utf8')
            response.connection.close()

            if 'Please enter another name.' in content:
                return None

            data = {
                'name': name,
                'start': start,
                'sex': sex,
                'rankings': [],
            }

            soup = BeautifulSoup(content,'html.parser')
            rows = soup.find_all('tr', {'valign': 'bottom'})

            for row in rows:
                tds = row.find_all('td', {'align': 'center'})
                data['rankings'].append({
                    'year': int(tds[0].text),
                    'rank': int(tds[1].text),
                })

            self._cache_store_(parameters, data)

        return data

