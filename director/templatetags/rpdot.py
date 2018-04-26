"""
not use
"""

#from django.core.serializers import serialize
#from django.db.models.query import QuerySet, ValuesListQuerySet
#from django.utils.safestring import mark_safe
from django.template import Library
from django.utils.safestring import mark_safe



register = Library()

def rpdot(obj):
    if obj is None:
        return ''
    else:
        return obj.replace('.','_')
        #outstr=json.dumps(obj)
        #return mark_safe( outstr )

    #if isinstance(object, ValuesListQuerySet):
        #return mark_safe(json.dumps(list(object)))
    #if isinstance(object, QuerySet):
        #return mark_safe(serialize('json', object))
    #return mark_safe(json.dumps(object))

register.filter('rpdot', rpdot, is_safe=True)
#jsonify.is_safe = True  