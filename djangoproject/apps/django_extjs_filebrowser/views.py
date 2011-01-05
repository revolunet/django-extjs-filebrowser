from settings import sources
from django.conf import settings
from django.http import HttpResponse
from core import utils, decorators
import os
import datetime




def dirToJson( inFs, path = '/', recursive = False):
    data = []
    for item in inFs.listdir(path = path ):
        fPath =  os.path.join(path, item ) 
        infos = inFs.getinfo( fPath )
        isLeaf = not inFs.isdir( fPath )
       
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
            row['items'] = dirToJson(inFs, path = fPath, recursive = recursive )
           
        data.append( row )
    return data
    
def example( request ):
    d = { }
    return utils.renderWithContext(request, 'example.html', d ) 
    
def splitPath( inPath ):
    if not inPath:
        return None, None
    if inPath[0] == '/':
        inPath = inPath[1:]
    root = inPath.split('/')[0]
    path = '/'.join(inPath.split('/')[1:])
    return root, path
    
def getFsFromKey( key ):
    source = sources[key]
    cur_fs = source['cls']( **source['params'] )
    return cur_fs
    
@decorators.ajax_request
def api( request ):
    cmd = request.POST.get('cmd', request.GET.get('cmd'))
    if not cmd:
        raise Http404
    
    # todo: remove these special cases
    if cmd == 'delete':
        root, path = splitPath( request.POST['file'] )
    elif cmd in ['view', 'download']:
        root, path = splitPath( request.GET['file'] )
    elif cmd == 'rename':
        root, path = splitPath( request.POST['oldname'] )
    else:
        root, path = splitPath( request.POST['path'] )
        
    if root:
        cur_fs = getFsFromKey( root )
    
    if cmd == 'get':
        if not root:
            items = []
            for item in sources.keys():
                row = {
                    'text':item
                    ,'size':0
                    ,'iconCls':'test'
                    ,'modified_time':''
                    ,'created_time':''
                    ,'leaf':False
                }
                items.append( row )
            return items
        return dirToJson( cur_fs, path, recursive = False )
    elif cmd == 'newdir':
        cur_fs.makedir( path )
        return {'success':True}
    elif cmd == 'rename':
        # todo : handle FS level moves
        root2, path2 = splitPath( request.POST['newname'] )
        if root == root2:
            # same FS
            cur_fs.rename( path, path2 )
        else:
            # different FS
            cur_fs2 = getFsFromKey( root2 )
            inFile = cur_fs.open( path, 'rb' )
            outFile = cur_fs2.open( path2, 'wb' ) 
            outFile.write( inFile.read() )
            outFile.close()
            
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

    
    
 
@decorators.swfupload_cookies_auth
@decorators.ajax_request    
def upload(request): 
    path = request.META.get('HTTP_X_FILE_NAME')

    file_list = []
    filename_list = []
    
    allowed_extensions = 'jpg,jpeg,gif,png,pdf,swf,avi,mp4,mp3,flv,doc,docx,xls,xlsx,ppt,pptx'.split(',')

    if path and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        root, path = splitPath( path.decode('UTF-8') )
        cur_fs = getFsFromKey( root )
        data = request.raw_post_data
        fName = path
        if not fName[fName.rfind('.')+1:].lower() in allowed_extensions:
            print 'FORBIDDEN FILE : %s ' % fName
            raise Exception('extension not allowed %s' % fName)
        f = cur_fs.open( path, 'wb')
        f.write(data)
        f.close()

    else:
        root, path = splitPath( request.POST['path'].decode('UTF-8') )
        cur_fs = getFsFromKey( root )
        for key in request.FILES.keys():
            upload = request.FILES[key]
            fName = upload.name
            # check extensions
            if not fName[fName.rfind('.')+1:].lower() in allowed_extensions:
                # todo : log + mail
                print 'FORBIDDEN FILE : %s ' % fName.encode('UTF-8')
                raise Exception('extension not allowed %s' % fName.encode('UTF-8'))
            f = cur_fs.open( path + '/' + fName, 'wb')
            for chunk in upload.chunks():
                f.write(chunk)
            f.close()         
            
    return {'success':True, 'files':file_list}
 