from settings import sources
from django.conf import settings
from django.http import HttpResponse
from core import utils, decorators
import os

def dirToJson( inFs, path = '/', recursive = False):
    print 'dirToJson', path
    data = []
    for item in inFs.listdir(path = path ):
        infos = inFs.getinfo( os.path.join(path, item ) )
        isLeaf = not inFs.isdir( item )
        row = {
            'text':item
            ,'size':infos['size']
            ,'modified_time':infos['modified_time'].isoformat()
            ,'created_time':infos['created_time'].isoformat()
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
    
@decorators.ajax_request
def api( request ):
    cmd = request.POST['cmd']
    path = request.POST['path'].split('/')[0]
    
    folder = sources[path]    
    from fs.osfs import OSFS
    cur_fs = OSFS(folder)
    
    if cmd == 'get':
        print 1
        return {'data':dirToJson( cur_fs, recursive = True )}
    elif cmd == 'newdir':
        remaning = '/'.join(request.POST['path'].split('/')[1:])
        print 'newdir', request.POST['path'], remaning
        cur_fs.makedir(remaning)
        return {'success':True}
    elif cmd == 'rename':
        print 'rename', path
    elif cmd == 'delete':
        print 'delete', path
    elif cmd == 'view':
        print 'view', path
    return {'success':False, msg:'Erreur'}
    
@decorators.ajax_request    
def upload( request ):
    return HttpResponse('api')