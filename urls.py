from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
     (r'filebrowser/api', views.api, {}, 'filebrowser-api'),
     (r'filebrowser/upload', views.upload, {}, 'filebrowser-api-upload'),
     (r'filebrowser/example', views.example, {}, 'filebrowser-example'),

) 
 