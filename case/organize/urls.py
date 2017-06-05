from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^department$',views.manage_department,name='organize.department'),
    # url(r'^model/(?P<name>.*)/$', views.model_view),
]