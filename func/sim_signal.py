from functools import wraps

class SimSignal(object):
    def __init__(self): 
        self.map_dict = {}
        
    def connect(self, msg, fun): 
        if msg not in self.map_dict:
            self.map_dict[msg] = []
        self.map_dict[msg].append(fun)
    
    def send(self, msg, *args, **kws): 
        ls = self.map_dict.get(msg, [])
        for fun in ls:
            fun(*args, **kws)
        # 返回 函数列表便于调试
        return ls
    
    def recieve(self, msg): 
        def decorator(fun):
            self.connect(msg, fun)
            @wraps(fun)
            def wrapper(*args, **kw):
                return fun(*args, **kw)
            return wrapper
        return decorator        

sim_signal = SimSignal()