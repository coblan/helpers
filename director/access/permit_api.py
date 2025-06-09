from helpers.director.shortcut import director_element,get_request_cache
from . permit import user_permit_names
from helpers.director.decorator import need_login


@director_element('permit')
class PermitApi(object):
    public_api=['userPermit']
    @need_login
    def userPermit(self):
        user = get_request_cache()['request'].user
        if user.is_superuser:
            ls = ['is_superuser']
        else:
            ls = list(set( user_permit_names(user) ) ) 
        return ls