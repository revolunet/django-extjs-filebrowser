# -*- encoding: utf-8 -*-



# some common routines
#

import os
import re
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_list_or_404
from django.utils import simplejson
from django.conf import settings

class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data):
        super(JsonResponse, self).__init__(content=simplejson.dumps(data), mimetype='application/json')


        
def renderWithContext(request, model, data={}, mimetype = None):
    ctx = RequestContext(request)
    data['settings']=settings
    return render_to_response(model, data, context_instance=ctx, mimetype = mimetype)
     
