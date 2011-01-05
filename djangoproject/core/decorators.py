
from django.utils.functional import wraps
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf import settings

import utils

__all__ = ['ajax_request']


def ajax_request(func):
    """
    If view returned serializable dict, returns JsonResponse with this dict as content.

    example:
        
        @ajax_request
        def my_view(request):
            news = News.objects.all()
            news_titles = [entry.title for entry in news]
            return {'news_titles': news_titles}
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, dict):
            return utils.JsonResponse(response)
        elif isinstance(response, list):
            return utils.JsonResponse(response)
        else:
            return response
    return wrapper  
    
    
def swfupload_cookies_auth(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        given_session = request.POST.get(settings.SESSION_COOKIE_NAME)
        if given_session:
            session = get_object_or_404(Session, session_key=given_session)
            session_data = session.get_decoded()
            if not session_data.has_key('_auth_user_id'):
                # not auth but sent an invalid sessionid
                raise Http404()
            user = get_object_or_404(User, pk = session_data['_auth_user_id'])
            request.user = user
        return function(request, *args, **kwargs)
    return wrap
