class Usage (Exception):
    """
        This exception is fired when a function is 
        used in the wrong way.
    """
    def __init__(self,msg):
        self.msg = msg

class DataStoreClash (Exception):
    """
        This exception is fired when an add fails
        due to a clash.
    """
    def __init__(self, entity):
        self.entity = entity
