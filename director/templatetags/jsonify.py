#from django.core.serializers import serialize
#from django.db.models.query import QuerySet, ValuesListQuerySet
#from django.utils.safestring import mark_safe
from django.template import Library
from django.utils.safestring import mark_safe
from ..data_format.json_format import DirectorEncoder
import json
import re

register = Library()

replace_script = re.compile('<(/script>)',flags=re.IGNORECASE)
def jsonify(obj):
    if obj is None:
        return ''
    else:
        outstr=json.dumps(obj,cls=DirectorEncoder,ensure_ascii=False)
        #'<' + '/script>'
        #outstr = outstr.replace('</script>','<" + "/script>')
        #outstr = aa.sub('<" + "/script>',outstr)  # outstr.replace('</script>','<" + "/script>')
        outstr = replace_script .sub('<" + "\g<1>',outstr) 
        outstr =  mark_safe( outstr )
        
        return outstr

    #if isinstance(object, ValuesListQuerySet):
        #return mark_safe(json.dumps(list(object)))
    #if isinstance(object, QuerySet):
        #return mark_safe(serialize('json', object))
    #return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify, is_safe=True)
#jsonify.is_safe = True  