import requests
import pandas as pd
import sqlalchemy
import os


class Country(object):

    def __init__(self):
        self._url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
        self.coordinate = 0
        self.lat = 0
        self.long = 0

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        if (value < -90) or (value > 90):
            raise ValueError("latitude value exceeds bound (-90,90)")
        self._lat = value

    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, value):
        if (value < -180) or (value > 180):
            raise ValueError("longitude value exceeds bound (-180,80)")
        self._long = value


    def get_coordinate(self, country):
        """
        :param country (string)
        :return: coordinate [x, y]. x is the latitude and y is the longitude.

        This function will return coordinate of the input country.
        """
        access_token = os.getenv('access_token')
        country = country + '.json'
        params = {'limit': 1,
                  #'types': 'country&region',
                  'access_token': access_token}
        r = requests.get(url=self._url + country, params=params)
        r_dict = r.json()
        self.coordinate = r_dict['features'][0]['center']
        self.lat, self.long = self.coordinate
        return self.lat, self.long

class Country_latlong(Country):
    def __init__(self):
        super(Country_latlong, self).__init__()
        self.country_dict = {}
        self.latlist = []
        self.longlist = []


    def create_table(self):
        """
        :return: a table has 5 columns id, country_id, country_name, lat, and long.
        """
        #connect to database.sqlite and extract table "country"
        engine = sqlalchemy.create_engine('sqlite:///database.sqlite')
        conn = engine.connect()
        table_country = pd.read_sql("""select * from Country """, engine)

        #create table latlong
        meta = sqlalchemy.MetaData(engine)
        table = sqlalchemy.Table('latlong', meta,
                      sqlalchemy.Column('id', sqlalchemy.Integer(), primary_key=True),
                      sqlalchemy.Column('country_id', sqlalchemy.Integer()),
                      sqlalchemy.Column('country_name', sqlalchemy.String()),
                      sqlalchemy.Column('lat', sqlalchemy.Float()),
                      sqlalchemy.Column('long', sqlalchemy.Float())
                        )
        meta.create_all()

        #insert multiple data
        idlist = list(range(table_country.shape[0]))
        country_id = table_country['id'].tolist()
        country_name = table_country['name'].tolist()
        [self.latlist.append(self.get_coordinate(country)[0]) for country in country_name]
        [self.longlist.append(self.get_coordinate(country)[1]) for country in country_name]

        self.country_dict = [{'id': ids, 'country_id': cid, 'country_name': cn, 'lat': la, 'long': lon} for (ids, cid, cn, la, lon) in
                        zip(idlist, country_id, country_name, self.latlist, self.longlist)]

        conn.execute(table.insert(), self.country_dict)


