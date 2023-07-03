import json  
from django.utils import timezone
from datetime import datetime,date,time
from decimal import Decimal
from django.conf import settings
import base64
from helpers.director.model_func.func import is_lazy_label


#if getattr(settings, 'GEO'):
    #from helpers.func.geo import poly2dict
#from django.contrib.gis.geos import Polygon


json_decoder = {
    bytes:lambda x: base64.b64encode(x).decode('utf-8')
}


class DirectorEncoder(json.JSONEncoder):  
    """
    Usage: json.dumps(value,cls=DirectorEncoder)
    """
    def default(self, obj):  
        if isinstance(obj, (timezone.datetime,datetime) ):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d")  
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj,time):
            return obj.strftime('%H:%M:%S')
        geo_rt = self.geoObj(obj)
        if geo_rt:
            return geo_rt
        #elif isinstance(obj,Point):
            #return '%s,%s'%(obj.y,obj.x)
        elif is_lazy_label(obj):
            # models.py里面的verbose_name使用的 django lazy_gettext 
            return str(obj)
        else:
            for cls, func in json_decoder.items():
                if isinstance(obj, cls):
                    return func(obj)
        #elif isinstance(obj,Polygon):
            #return poly2dict(obj) 
            return json.JSONEncoder.default(self, obj) 
    
    def geoObj(self,obj):
        try:
            if not getattr(self,'has_geo',True):
                return None
            from django.contrib.gis.geos.point import Point
            if isinstance(obj,Point):
                return '%s,%s'%(obj.y,obj.x)            
        except Exception:
            print('json no geo support')
            self.has_geo = False
        
    
