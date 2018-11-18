import json  
from django.utils import timezone
from datetime import datetime,date
from decimal import Decimal
from django.conf import settings

#if getattr(settings, 'GEO'):
    #from helpers.func.geo import poly2dict
#from django.contrib.gis.geos import Polygon

json_decoder = {
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
        else:
            for cls, func in json_decoder.items():
                if isinstance(obj, cls):
                    return func(obj)
        #elif isinstance(obj,Polygon):
            #return poly2dict(obj) 
            return json.JSONEncoder.default(self, obj) 
        
