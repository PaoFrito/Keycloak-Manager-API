import json

def dict2obj(dict, cls):
    
    class obj(cls):
        def __init__(self, dict_):
            self.__dict__.update(dict_)
        
    return json.loads(json.dumps(dict), object_hook=obj)