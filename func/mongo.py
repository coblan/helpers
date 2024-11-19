import datetime
from pymongo import UpdateOne

beijin = datetime.timezone(datetime.timedelta(hours=8))
utc = datetime.timezone(datetime.timedelta(hours=0))

def tm2mongo(dt):
    if not dt:
        return dt
    tmp = dt.replace(tzinfo=beijin)
    return tmp

def mongo2tm(dt):
    if not dt:
        return dt
    dd = dt.replace(tzinfo=utc)
    return dd.astimezone(beijin)

def get_or_create(model,defaults={},**kws):
    #inst = model.objects.filter(**kws).first()
    try:
        inst = model.objects.get(**kws)
        return inst
    except model.DoesNotExist:
        ff = kws.copy()
        ff.update(defaults)
        return model.objects.create(**ff)
    #else:
        #VideoTagIndexTest.objects.create(mid=302)
        #return model(**kws)

def filter_update(model,update_list):
    """
    update_list:[{'filter':{},'set':{},'add':{},'add_to_set':{}}]
    文档参考：
    https://www.mongodb.com/docs/manual/reference/operator/update/#std-label-update-operators
    """
    bulk_operations = []
   
    for update_dc in update_list:
        update_dict = {}
        if update_dc.get('set'):
            update_dict['$set'] = update_dc.get('set')
        if update_dc.get('add'):
            """
            {$push:{content:{'$each':[1,2,3]}} }
            """
            push_dict = {}
            for k,v in update_dc.get('add').items():
                push_dict[k] = {'$each':v}
            update_dict['$push'] =push_dict   #{'$each':update_dc.get('add')} 
        
        if update_dc.get('add_to_set'):
            """
            {$addToSet:{content:{'$each':[1,2,3]}} }
            """
            push_dict = {}
            for k,v in update_dc.get('add_to_set').items():
                push_dict[k] = {'$each':v}
            update_dict['$addToSet'] =push_dict         
            
        bulk_operations.append(
            UpdateOne(update_dc.get('filter'), 
                      update_dict
                      ,upsert=True)
        )
        
        #if update_fields:
            #dc = {field_name:getattr(instance,field_name) for field_name in update_fields}
        #else:
            #dc = instance.to_mongo().to_dict()
        #bulk_operations.append(
            #UpdateOne({'_id': instance._id}, {'$set': dc},upsert=True)
        #)
    
    if bulk_operations:
        collection = model._get_collection() \
            .bulk_write(bulk_operations, ordered=False)  
        return collection
    
