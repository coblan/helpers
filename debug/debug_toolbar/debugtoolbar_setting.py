
def SET(scope):
    scope['DEBUG_TOOLBAR']=True
    scope['INSTALLED_APPS'].extend(['debug_toolbar',])
    scope['MIDDLEWARE_CLASSES'].extend([
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'helpers.debug.debug_toolbar.json_as_html.JsonAsHTML',
        
        ])
    scope['INTERNAL_IPS'] =['127.0.0.1']


def AUTO_URL(scope):
    from django.conf.urls import url,include
    from django.conf import settings
    if settings.DEBUG and getattr(settings,'DEBUG_TOOLBAR',None):
        import debug_toolbar
        scope['urlpatterns'] += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    