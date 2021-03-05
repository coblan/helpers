"""
1.
pip install django_debug_toolbar

2. in settings.py 
from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import SET
SET(globals()) 

3. in urls.py
from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import AUTO_URL
AUTO_URL(globals())

"""
def SET(scope):
    scope['DEBUG_TOOLBAR']=True
    scope['INSTALLED_APPS'].extend(['debug_toolbar',])
    if 'MIDDLEWARE_CLASSES' in scope:
        scope['MIDDLEWARE_CLASSES'].extend([
            'debug_toolbar.middleware.DebugToolbarMiddleware',
            'helpers.maintenance.debug.debug_toolbar.json_as_html.JsonAsHTML',
            ])
    else:
        scope['MIDDLEWARE'].extend( [
            'debug_toolbar.middleware.DebugToolbarMiddleware',
            'helpers.maintenance.debug.debug_toolbar.json_as_html.JsonAsHTML',
        ]   )
 
    #scope['DEBUG_TOOLBAR_CONFIG'] ={}

    scope['INTERNAL_IPS'] =['127.0.0.1']
    DEBUG_TOOLBAR_PANELS = [
        'ddt_request_history.panels.request_history.RequestHistoryPanel',  # Here it is 
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        #'debug_toolbar.panels.templates.TemplatesPanel',
        #'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
    scope['DEBUG_TOOLBAR_PANELS']=DEBUG_TOOLBAR_PANELS



def AUTO_URL(scope):
    from django.conf.urls import url,include
    from django.conf import settings
    if settings.DEBUG and getattr(settings,'DEBUG_TOOLBAR',None):
        import debug_toolbar
        scope['urlpatterns'] += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    