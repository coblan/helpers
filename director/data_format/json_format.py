import json  
from django.utils import timezone
from datetime import datetime,date
from decimal import Decimal
from helpers.func.geo import poly2dict
from django.contrib.gis.geos import Polygon

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
        elif isinstance(obj,Polygon):
            return poly2dict(obj)
        else:  
            return json.JSONEncoder.default(self, obj) 
        
def poly2dict(polygon_obj):
    """
    将models.PolygonField对象转换为高德地图能够接受的坐标列表
    
    @polygon_obj: models.PolygonField对象
    
    """
    if polygon_obj:
        polygon_arr = list(polygon_obj.coords[0])
        polygon_arr.pop()
        return polygon_arr
    else:
        return []

def dict2poly(arr):
    if arr:
        if arr[-1] != arr[0]:
            arr.append(arr[0])
        poly = Polygon(arr)
        poly.srid=4326
        return poly
    else:
        return None   