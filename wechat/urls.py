"""
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'pay/reply',views.pay_replay,name='wepay_relay'),
    url(r'pay/new_order',views.wepay_make_order),

]
