import json
import requests
from .exceptions import DaqssException, DaqssRequestError

class Daqss(object):
    def __init__(self, apikey = None, apipswd = None, version = 'v1.0'):
        self.apikey = apikey
        self.apipswd = apipswd
        self.authenticated = False
        self.api_version = version
        self.base_url = 'http://45.55.154.140/api/'
        self._headers = {'content-type': 'application/json'}
        
        # endpoints
        self._endpoints = {
            'check_authentication': 'auth/',
            'nodes': 'nodes/',
            'ind_node': 'nodes/',
            'as': 'alphasense/',
            'ind_as': 'alphasense/',
            'as_data': 'alphasense/data/',
            'add_as': 'alphasense/data/',
            'rht': 'rht/',
            'ind_rht': 'rht/',
            'rht_data': 'rht/data/',
            'add_rht': 'rht/data/'
        }
        
    def _make_endpoint(self, endpoint, **kwargs):
        id = kwargs.get('id', None)
        page = kwargs.get('page', None)
        
        if endpoint == 'ind_node' or endpoint == 'ind_as' or endpoint == 'ind_rht':
            if id is None:
                raise DaqssException("ID must be set to get an individual node.")
            else:
                return "{0}{1}/{2}{3}".format(self.base_url, 
                                           self.api_version, self._endpoints[endpoint], id)
            
        if endpoint == 'as_data' or endpoint == 'rht_data':
            return "{0}{1}/{2}{3}/{4}".format(self.base_url, self.api_version, self._endpoints[endpoint], id, page)
        
        if endpoint == 'add_rht' or endpoint == 'add_as':
            return "{0}{1}/{2}".format(self.base_url, self.api_version, self._endpoints[endpoint])

        return "{0}{1}/{2}".format(self.base_url, self.api_version, self._endpoints[endpoint])
    
    def _getcall(self, endpoint, id = None, page = None):
        try:
            req = requests.get(self._make_endpoint(endpoint, id = id, page = page), 
                               auth = (self.apikey, self.apipswd), headers = self._headers)
        except Exception as e:
            raise DaqssRequestError(e)
            
        return req
    
    def _postcall(self, endpoint, id = None, data = None):
        ''' Makes a post call [Add in error checking to throw various exceptions ]'''
        try:
            req = requests.post(self._make_endpoint(endpoint, id = id), 
                               auth = (self.apikey, self.apipswd), headers = self._headers, data = data)
        except Exception as e:
            raise DaqssRequestError(e)
            
        return req
    
    def _putcall(self, endpoint, id = None, data = None):
        ''' Edits a node in the database '''
        try:
            req = requests.put(self._make_endpoint(endpoint, id = id), 
                               auth = (self.apikey, self.apipswd), headers = self._headers, data = data)
        except Exception as e:
            raise DaqssRequestError(e)
            
        return req
    
    def _deletecall(self, endpoint, id = None):
        ''' Drops a node from the database '''
        try:
            req = requests.delete(self._make_endpoint(endpoint, id = id),
                                 auth = (self.apikey, self.apipswd), headers = headers)
        except Exception as e:
            raise DaqssRequestError(e)
            
        return req
        
    def ping(self):
        ''' Pings the server and returns True if authentication credentials are legit '''
        r = self._getcall('check_authentication')
        if r.status_code == 200:
            return True
        else:
            return False
        
    def nodes(self):
        ''' Gets response for all nodes '''
        r = self._getcall('nodes')
        if r.status_code == 200:
            pass
        else:
            raise DaqssException(r.status_code)
            
        return r.status_code, r.json()
    
    def node(self, id = None):
        ''' Gets data for an individual node set by id '''
        if id is None:
            raise DaqssException("ID is required")
            
        r = self._getcall('ind_node', id = id)
            
        return r.status_code, r.json()
    
    def addNode(self, data):
        ''' Adds a node to the network '''
        r = self._postcall('nodes', data = json.dumps(data))
        
        return r.status_code, r.json()
    
    def editNode(self, id, data):
        r = self._putcall('ind_node', id = id, data = json.dumps(data))
        
        return r.status_code, r.json()
    
    def dropNode(self, id):
        r = self._deletecall('ind_node', id = id)
        
        return r.status_code, r.json()
    
    def sensors(self):
        ''' Grabs all alphasense sensors '''
        r = self._getcall('as')
        
        return r.status_code, r.json()
    
    def sensor(self, id = None):
        ''' Get individual sensor '''
        if id is None:
            raise DaqssException("ID is required.")
            
        r = self._getcall('ind_as', id = id)
        
        return r.status_code, r.json()
    
    def sensorData(self, id = None, page = 1):
        ''' Gets the data for an individual Alphasense sensor '''
        if id is None:
            raise DaqssException("ID is required")
            
        r = self._getcall('as_data', id = id, page = page)
        
        return r.status_code, r.json()
    
    def addSensor(self, data):
        ''' Adds an Alphasense sensor to the network '''
        r = self._postcall('as', data = json.dumps(data))
        
        return r.status_code, r.json()
    
    def editSensor(self, id, data):
        r = self._putcall('ind_as', id = id, data = json.dumps(data))
        
        return r.status_code, r.json()
    
    def dropSensor(self, id):
        ''' Deletes a sensor '''
        r = self._deletecall('ind_as', id = id)
        
        return r.status_code, r.json()

    def addASData(self, data):
        ''' Add Alphasense Data '''
        r = self._postcall('add_as', data)

        return r.status_code, r.json()
    
    def rhts(self):
        ''' Returns all RHT sensors '''
        r = self._getcall('rht')
        
        return r.status_code, r.json()
    
    def rht(self, id = None):
        ''' Returns information about a single RHT Sensor '''
        if id is None:
            raise DaqssException("ID is required.")
        
        r = self._getcall('ind_rht', id = id)
        
        return r.status_code, r.json()
    
    def rhtData(self, id = None, page = 1):
        ''' Gets the data for an individual RHT sensor '''
        if id is None:
            raise DaqssException("ID is required")
            
        r = self._getcall('rht_data', id = id, page = page)
        
        return r.status_code, r.json()
    
    def addRHT(self, data):
        ''' Adds an RHT sensor to the network '''
        r = self._postcall('rht', data = json.dumps(data))
        
        return r.status_code, r.json()
    
    def editRHT(self, id, data):
        ''' Edits an RHT Sensor '''
        r = self._putcall('ind_rht', id = id, data = json.dumps(data))
        
        return r.status_code, r.json()
    
    def dropRHT(self, id):
        ''' Deletes an RHT sensor '''
        r = self._deletecall('ind_rht', id = id)
        
        return r.status_code, r.json()

    def addRHTData(self, data):
        ''' Allows us to add a new RHT Data point '''
        r = self._postcall('add_rht', data = data)

        return r.status_code, r.json()
    
    def __repr__(self):
        return "Daqss Auth: {0}".format(self.authenticated)