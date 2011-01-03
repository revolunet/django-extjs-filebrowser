# -*- encoding: utf-8 -*-


# some common routines
#

import os
import re
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_list_or_404


def renderWithContext(request, model, data={}, mimetype = None):
    ctx = RequestContext(request)
    return render_to_response(model, data, context_instance=ctx, mimetype = mimetype)
     
