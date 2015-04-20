class DaqssException(Exception):
    def __init__(self, obj):
        self.obj = obj
        
    def __str__(self):
        return "DAQSS Error: {0}".format(self.obj)
    
class DaqssRequestError(Exception):
    def __init__(self, exc):
        self.exc = exc
        
    def __str__(self):
        return "Caught exception {0} with error: {1}".format(type(self.exc), self.exc)