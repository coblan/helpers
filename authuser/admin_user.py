from helpers.director.shortcut import director_view,get_request_cache
from helpers.director.decorator import need_login

@director_view('user/info')
@need_login
def user_info():
    user = get_request_cache()['request'].user
    return {
        'username':user.username,
        'nickname':user.first_name,
        'head':user.last_name,
        'email':user.email,
    }