from settings import sources
from django.conf import settings
from django.http import HttpResponse
from core import utils
import os

def dirToJson( inFs, path = '/', recursive = False):
    print 'dirToJson', path
    data = []
    for item in inFs.listdir(path = path ):
        infos = inFs.getinfo( os.path.join(path, item ) )
        isLeaf = not inFs.isdir( item )
        row = {
            'name':item
            ,'size':infos['size']
            ,'modified_time':infos['modified_time']
            ,'created_time':infos['created_time']
            ,'leaf':isLeaf
            ,'items':[]
        }
        # recursive and isdir ? 
        if not isLeaf and recursive:
            row['items'] = dirToJson(inFs, path = os.path.join(path, item), recursive = recursive )
           
        data.append( row )
    return data
    
def example( request ):
    d = {
        
    }
    return utils.renderWithContext(request, 'example.html', d ) 
    
    
def api( request ):
    cmd = request.POST['cmd']
    path = request.POST['path']
    
    folder = sources[path]
    
    from fs.osfs import OSFS
    cur_fs = OSFS(folder)
    print dirToJson( cur_fs, recursive = True )
    return HttpResponse('api')
    
    
def upload( request ):
    return HttpResponse('api')