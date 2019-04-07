
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from helpers.director.model_func.field_proc  import BaseFieldProc
from helpers.director.shortcut import field_map

class CusPointProc(BaseFieldProc):
    
    def to_dict(self,inst,name):
        data = getattr(inst,name)
        field = inst.__class__._meta.get_field(name)
        if data:
            return {name: (data.x,data.y)}
        else:
            return {name: ''}
    
    def clean_field(self,dc,name):
        if dc.get(name):
            ls=dc.get(name)
            pp = Point(x=float(ls[0]),y=float(ls[1]))
            pp.srid=4326
            return pp
        else:
            return dc.get(name)
    
field_map.update({
    models.PointField:CusPointProc
})