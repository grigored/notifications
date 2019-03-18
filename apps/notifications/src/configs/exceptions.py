class OwnException(Exception):
    def __init__(self, message, data=None, **kwargs):
        self.message = message
        self.data = data
        for attr in kwargs:
            setattr(self, attr, kwargs.get(attr))
