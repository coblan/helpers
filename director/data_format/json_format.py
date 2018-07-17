import json  
from django.utils import timezone
from datetime import datetime,date
from decimal import Decimal
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
            return json.JSONEncoder.default(self, obj) 