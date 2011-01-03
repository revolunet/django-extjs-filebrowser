from django.conf.urls.defaults import *



from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
     (r'filebrowser/api', views.api, {}, 'filebrowser-api'),
     (r'filebrowser/upload', views.upload, {}, 'filebrowser-api-upload'),

     
) 
 