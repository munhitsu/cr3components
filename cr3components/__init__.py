class GlobalSettings:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state

    def __setitem__(self, key, item):
        self.__dict__.__setitem__(key, item)
    
    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)

    def items(self):
        return self.__dict__.items()