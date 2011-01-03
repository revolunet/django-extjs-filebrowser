
from django.http import HttpResponse
from core import utils

def example( request ):
    d = {
        settings:
    }
    return utils.renderWithContext(request, 'example.html', d ) 