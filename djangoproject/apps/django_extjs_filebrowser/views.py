from settings import sources
from django.conf import settings
from django.http import HttpResponse
from core import utils, decorators
import os
import datetime




def dirToJson( inFs, path = '/', recursive = False):
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
    if not inPath:
        return None, None
    if inPath[0] == '/':
        inPath = inPath[1:]
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
        
    if root:
        source = sources[root]
        cur_fs = source['cls']( **source['params'] )
    
    if cmd == 'get':
        if not root:
            items = []
            for item in sources.keys():
                row = {
                    'text':item
                    ,'size':0
                    ,'modified_time':''
                    ,'created_time':''
                    ,'leaf':False
                }
                items.append( row )
            return items
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
    
    

@decorators.swfupload_cookies_auth
@decorators.ajax_request    
def upload(request): 
    path = request.META['X-File-Name']
    root, path = splitPath( path )
    file_list = []
    filename_list = []
    
    allowed_extensions = 'jpg,jpeg,gif,png,pdf,swf,avi,mp4,mp3,flv,doc,docx,xls,xlsx,ppt,pptx'.split(',')
    
    print root, path
    return {'success':True, 'files':file_list}

    outPath = u'%s' % translateUserPath(request.user, path)

    if not os.path.isdir(outPath):
        os.makedirs(outPath)
    if request.GET.get('from') == 'screenshot':
        outPath = os.path.join( settings.DATA_PATH, 'public', 'user', str(request.user.id), 'screenshots' )
        if not os.path.isdir(outPath):
            os.makedirs(outPath)
        image_64 = request.raw_post_data
        if image_64:
            fName ="%s.jpg" % datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            dstFile = os.path.join(outPath, fName)
            data = base64.b64decode(image_64)
            dest = open(dstFile, 'wb')
            dest.write(data)
            dest.close()  
            file_list.append(dstFile)
            filename_list.append({'file': '/static%s/screenshots/%s' % (get_relative_user_path( request.user.id ), fName)})
    elif request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # htmL5 upload
        data = request.raw_post_data

        fName = request.META['HTTP_X_FILE_NAME'].decode('UTF-8')

        if not os.path.splitext(fName)[1].lower()[1:] in allowed_extensions:
            # todo : log + mail
            print 'FORBIDDEN FILE : %s ' % fName.encode('UTF-8')
            raise Exception('extension not allowed %s' % fName)
        dstFile = u'%s' % os.path.join(outPath, fName)
        utils.CheckPathSecurity(dstFile, outPath)
        dest = open(dstFile, 'wb')
        dest.write(data)
        dest.close()  
        file_list.append(dstFile)
        filename_list.append({'file':os.path.split(fName)[1]})
    else:
        # standard multipart upload
        for key in request.FILES.keys():
            upload = request.FILES[key]
            fName = upload.name
            # check extensions
            if not os.path.splitext(fName)[1].lower()[1:] in allowed_extensions:
                # todo : log + mail
                print 'FORBIDDEN FILE : %s ' % fName.encode('UTF-8')
                raise Exception('extension not allowed %s' % fName.encode('UTF-8'))
            dstFile = os.path.join(outPath, fName)
            #print dstFile, outPath
            utils.CheckPathSecurity( dstFile, outPath)
            #new_name = utils.guessNextPath(dstFile, slugify = True)
            dest = open(dstFile, 'wb')
            for chunk in upload.chunks():
                dest.write(chunk)
            dest.close()         
            
            file_list.append(dstFile)            
            filename_list.append({'file':os.path.split(fName)[1]})
            
    for fName in file_list:
        # PDF 2 jpg conversion

        # gdocs upload
        if os.path.splitext(fName)[1][1:] in 'xls,xlsx'.split(','):
            gurl = gapps.upload( fName, os.path.basename( fName ) )
            # create .gdocs.xls
            if gurl:
                linkfile = os.path.join( os.path.dirname( fName ), '%s.gdocs.xls' % os.path.basename( fName ) )
                open(linkfile, 'w').write('%s&chrome=false' % gurl)
                #f.close()
                # delete original
                os.remove( fName )
                # wait a while TODO
                time.sleep(3)
        else:
            f = converters.FileObject( fName )
            res = f.convert()
            if not res:
                return extutils.JsonError(_(u'Impossible de convertir ce fichier') )
                
    r = extutils.JsonSuccess({"files":filename_list})
    r['Content-Type'] = "text/html"
    #import time
    #time.sleep(5)
    return r