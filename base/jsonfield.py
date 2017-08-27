from django.db import models
import json

class JsonField(models.TextField):
    def  from_db_value(self,value, expression, connection,ctx):
        return json.loads(value)
    
    def get_prep_value(self,value):
        return json.dumps(value)