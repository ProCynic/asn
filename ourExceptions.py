class Usage (Exception):
    def __init__(self,msg):
        self.msg = msg

class DataStoreClash (Exception):
    def __init__(self, entity):
        self.entity = entity
