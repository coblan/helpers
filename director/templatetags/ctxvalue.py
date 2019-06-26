#from django.core.serializers import serialize
#from django.db.models.query import QuerySet, ValuesListQuerySet
#from django.utils.safestring import mark_safe
from django.template import Library
from django.utils.safestring import mark_safe
from ..data_format.json_format import DirectorEncoder
import json

register = Library()

def ctxvalue(key,ctx):
    if key is None:
        return ''
    else:
        outstr=ctx.get(key,key)
        return mark_safe( outstr )

    #if isinstance(object, ValuesListQuerySet):
        #return mark_safe(json.dumps(list(object)))
    #if isinstance(object, QuerySet):
        #return mark_safe(serialize('json', object))
    #return mark_safe(json.dumps(object))

register.filter('ctxvalue', ctxvalue, is_safe=True)
#jsonify.is_safe = True  