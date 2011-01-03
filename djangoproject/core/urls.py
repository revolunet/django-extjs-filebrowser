import os
from django.conf.urls.defaults import *
from django.conf import settings

import statics_urls

urlpatterns = patterns('',)


# include statics
urlpatterns += patterns('',
     (r'', include(statics_urls)),
) 

# include urls.py inside apps if any
for file in os.listdir(os.path.join(settings.BASE_DIR, 'apps')):
    u = os.path.join(settings.BASE_DIR, 'apps', file, 'urls.py')
    if os.path.isfile(u):
        urlpatterns += patterns('', 
            (r'' , include('apps.%s.urls' % file)), 
        ) 
  
# auto apps includes
urlpatterns += patterns('',    
    (r'^apps/(?P<app>[^/]+)/(?P<view>[^/]+)/?(?P<path>.+)?$', 'core.appdispatcher.dispatch' ),
    (r'^apps/(?P<app>[^/]+)/?$', 'core.appdispatcher.dispatch' ),
)
 
# default fallback
urlpatterns += patterns('',
     (r'^$', settings.DEFAULT_VIEW),
) 


