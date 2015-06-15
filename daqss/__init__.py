import json
import requests
import datetime
from pkg_resources import get_distribution
from .exceptions import DaqssException, DaqssRequestError

__all__ = ['Daqss']
__version__ = get_distribution('daqss').version

class Daqss(object):
    def __init__(self, apikey = None, apipswd = None, version = 'v1.0'):
        self.apikey = apikey
        self.apipswd = apipswd
        self.authenticated = False
        self.api_version = version
        self.base_url = 'http://45.55.154.140/api/'
        self._headers = {'content-type': 'application/json'}

    def _make_endpoint(self, endpoint):
        ''' Makes the endpoint '''

        return "{0}{1}/{2}".format(self.base_url, self.api_version, endpoint)

    def _getcall(self, uri):
        try:
            req = requests.get(uri, auth = (self.apikey, self.apipswd),
                    headers = self._headers)
        except Exception as error:
            raise DaqssRequestError(error)

        return req

    def _postcall(self, endpoint, data):
        try:
            req = requests.post(endpoint, auth = (self.apikey, self.apipswd),
                                headers = self._headers, data = data)
        except Exception as error:
            raise DaqssRequestError(error)

        return req

    def _putcall(self, endpoint, data):
        try:
            req = requests.put(endpoint, auth = (self.apikey, self.apipswd),
                               headers = self._headers, data = data)
        except Exception as error:
            raise DaqssRequestError(error)

        return req

    def _deletecall(self, endpoint):
        try:
            req = requests.delete(endpoint, auth = (self.apikey, self.apipswd),
                                  headers = self._headers)
        except Exception as error:
            raise DaqssRequestError(error)

        return req

    def ping(self):
        ''' Pings the server and returns True if authentication credentials are legit '''
        r = self._getcall(self._make_endpoint('auth/'))
        if r.status_code == 200:
            return True
        else:
            return False

    def get_nodes(self):
        ''' Returns all nodes '''
        r = self._getcall(self._make_endpoint('nodes/'))

        return r.status_code, r.json()

    def get_node(self, sn):
        ''' Returns data for node with serial number `sn` '''
        r = self._getcall(self._make_endpoint('nodes/{0}'.format(sn)))

        return r.status_code, r.json()

    def add_node(self, data):
        ''' Adds a node to the network '''
        r = self._postcall(self._make_endpoint('nodes/'), data = json.dumps(data))

        return r.status_code, r.json()

    def edit_node(self, sn, data):
        ''' Edit a node '''
        r = self._putcall(self._make_endpoint('nodes/{0}'.format(sn)),
                          data = json.dumps(data))

        return r.status_code, r.json()

    def drop_node(self, sn):
        ''' Delete a node form the network '''
        r = self._deletecall(self._make_endpoint('nodes/{0}'.format(sn)))

        return r.status_code, r.json()

    def get_alphasense_sensors(self):
        ''' Grabs all alphasense sensors '''
        r = self._getcall(self._make_endpoint('alphasense/'))

        return r.status_code, r.json()

    def get_alphasense_sensor(self, id = None):
        ''' Get individual sensor '''
        r = self._getcall(self._make_endpoint('alphasense/{0}'.format(id)))

        return r.status_code, r.json()

    def get_alphasense_data(self, sn, basedate = None, enddate = None, period = None):
        ''' Gets the data for an individual Alphasense sensor '''
        if period is None:
            uri = self._make_endpoint('alphasense/{0}/data/date/{1}/{2}'.format(sn, basedate, enddate))
        else:
            uri = self._make_endpoint('alphasense/{0}/data/date/{1}/{2}'.format(sn, basedate, period))

        r = self._getcall(uri)

        return r.status_code, r.json()

    def add_alphasense(self, data):
        ''' Adds an Alphasense sensor to the network '''
        r = self._postcall(self._make_endpoint('alphasense'),
                            data = json.dumps(data))

        return r.status_code, r.json()

    def edit_alphasense(self, id, data):
        r = self._putcall(self._make_endpoint('alphasense/{0}'.format(id)),
                           data = json.dumps(data))

        return r.status_code, r.json()

    def drop_alphasense(self, id):
        ''' Deletes a sensor from the network '''
        r = self._deletecall(self._make_endpoint('alphasense/{0}'.format(id)))

        return r.status_code, r.json()

    def add_alphasense_data(self, data):
        ''' Add Alphasense Data '''
        r = self._postcall(self._make_endpoint('alphasense/data/'),
                            data = json.dumps(data))

        return r.status_code, r.json()

    def get_rhts(self):
        ''' Returns all RHT sensors '''
        r = self._getcall(self._make_endpoint('rht/'))

        return r.status_code, r.json()

    def get_rht(self, id):
        ''' Returns information about a single RHT Sensor '''
        r = self._getcall(self._make_endpoint('rht/{0}'.format(id)))

        return r.status_code, r.json()

    def get_rht_data(self, sn, basedate = None, enddate = None, period = None):
        ''' Gets the data for an individual RHT sensor '''
        if period is None:
            uri = self._make_endpoint('rht/{0}/data/date/{1}/{2}'.format(sn, basedate, enddate))
        else:
            uri = self._make_endpoint('rht/{0}/data/date/{1}/{2}'.format(sn, basedate, period))

        r = self._getcall(uri)

        return r.status_code, r.json()

    def add_rht(self, data):
        ''' Adds an RHT sensor to the network '''
        r = self._postcall(self._make_endpoint('rht/'), data = json.dumps(data))

        return r.status_code, r.json()

    def edit_rht(self, id, data):
        ''' Edits an RHT Sensor '''
        r = self._putcall(self._make_endpoint('rht/{0}'.format(id)),
                           data = json.dumps(data))

        return r.status_code, r.json()

    def drop_rht(self, id):
        ''' Deletes an RHT sensor '''
        r = self._deletecall(self._make_endpoint('rht/{0}'.format(id)))

        return r.status_code, r.json()

    def add_rht_data(self, data):
        ''' Allows us to add a new RHT Data point '''
        r = self._postcall(self._make_endpoint('rht/data/'),
                            data = json.dumps(data))

        return r.status_code, r.json()

    def get_opc(self, sn = None):
        '''
            If an id is passed, then just grab that one, otherwise return all opc.
            Include both the meta information as well as the data
        '''
        if sn is None:
            uri = self._make_endpoint('opc/')
        else:
            uri = self._make_endpoint('opc/{0}'.format(sn))

        r = self._getcall(uri)

        return r.status_code, r.json()

    def add_opc(self, data):
        ''' POST a new opc object '''
        uri = self._make_endpoint('opc/')
        r = self._postcall(uri, json.dumps(data))

        return r.status_code, r.json()

    def update_opc(self, sn, data):
        ''' Update the information on an existing OPC '''
        uri = self._make_endpoint('opc/{0}'.format(sn))

        r = self._putcall(uri, json.dumps(data))

        return r.status_code, r.json()

    def drop_opc(self, sn):
        ''' Delete the OPC '''
        uri = self._make_endpoint('opc/{0}'.format(sn))

        r = self._deletecall(uri)

        return r.status_code, r.json()

    def add_opc_config(self, data):
        ''' Add an opc config row '''
        uri = self._make_endpoint('opc/config/')
        r = self._postcall(uri, json.dumps(data))

        return r.status_code, r.json()

    def drop_opc_config(self, id):
        ''' Delete an opc config line '''
        uri = self._make_endpoint('opc/config/{0}'.format(id))
        r = self._deletecall(uri)

        return r.status_code, r.json()

    def add_opc_data(self, data):
        ''' Add a new opc data point '''
        uri = self._make_endpoint('opc/data/')
        r = self._postcall(uri, json.dumps(data))

        return r.status_code, r.json()

    def get_opc_data(self, sn, basedate = None, enddate = None, period = None):
        ''' Return the opc data paginated '''
        if period is None:
            uri = self._make_endpoint('opc/{0}/data/date/{1}/{2}'.format(sn, basedate, enddate))
        else:
            uri = self._make_endpoint('opc/{0}/data/date/{1}/{2}'.format(sn, basedate, period))

        r = self._getcall(uri)

        return r.status_code, r.json()

    def __repr__(self):
        return "Daqss Auth: {0}".format(self.authenticated)
