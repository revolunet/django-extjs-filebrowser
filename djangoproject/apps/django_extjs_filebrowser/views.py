from settings import sources
from django.conf import settings
from django.http import HttpResponse
from core import utils, decorators
import os
import datetime

def dirToJson( inFs, path = '/', recursive = False):
    print 'dirToJson', path
    data = []
    for item in inFs.listdir(path = path ):
        infos = inFs.getinfo( os.path.join(path, item ) )
        isLeaf = not inFs.isdir( item )
        print infos
        row = {
            'text':item
            ,'size':infos.get('size', 0)
            ,'modified_time':infos.get('modified_time', datetime.datetime.now()).isoformat()
            ,'created_time':infos.get('created_time', datetime.datetime.now()).isoformat()
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
    
def splitPath( inPath ):
    root = inPath.split('/')[0]
    path = '/'.join(inPath.split('/')[1:])
    return root, path
    
@decorators.ajax_request
def api( request ):
    cmd = request.POST.get('cmd', request.GET.get('cmd'))
    if not cmd:
        raise Http404
    
    # todo: remove these special cases
    if cmd == 'delete':
        root, path = splitPath( request.POST['file'] )
    if cmd in ['view', 'download']:
        root, path = splitPath( request.GET['file'] )
    elif cmd == 'rename':
        root, path = splitPath( request.POST['oldname'] )
    else:
        root, path = splitPath( request.POST['path'] )
        
    source = sources[root]
    cur_fs = source['cls']( **source['params'] )
    
    if cmd == 'get':
        return dirToJson( cur_fs, path, recursive = True )
    elif cmd == 'newdir':
        cur_fs.makedir( path )
        return {'success':True}
    elif cmd == 'rename':
        # todo : handle FS level moves
        root2, path2 = splitPath( request.POST['newname'] )
        cur_fs.rename( path, path2 )
        return {'success':True}
    elif cmd == 'delete':
        if cur_fs.isdir( path ):
            cur_fs.removedir( path )
        else:
            cur_fs.remove( path )
        return {'success':True}
    elif cmd == 'view':
        # todo redir to APACHE or OTHER
        file = cur_fs.open( path, 'rb' )
        return download( path, file)
    elif cmd == 'download':
        # todo redir to APACHE or OTHER
        #print 'download', root, path
        file = cur_fs.open( path, 'rb' )
        return download( path, file, attachment = True)
        
    return {'success':False, 'msg':'Erreur'}
    
def download( inFilePath, inFileObj, attachment = False ):
    import mimetypes
    inFileName = inFilePath.split('/')[-1]
    mt = mimetypes.guess_type(inFileName)
    response = HttpResponse(mimetype=mt)
    if attachment:
        response['Content-Disposition'] = 'attachment; filename=%s' % inFileName
    response.write( inFileObj.read() )
    return response

    
    
@decorators.ajax_request    
def upload( request ):
    return HttpResponse('api')