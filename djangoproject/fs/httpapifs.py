"""
fs.httpapifs
=========
wrapper for remote filesystems

julien@bouquillon.com
"""

from fs.base import FS
from fs.path import normpath
from fs.errors import ResourceNotFoundError, UnsupportedError
import urlparse 
import urllib2
from urllib import urlencode

from remote import CacheFS
import simplejson

import httplib, mimetypes

import cStringIO



import datetime


class _HTTPAPIFSFile(object):

    """ A file-like that provides access to a file with FileBrowser API"""

    def __init__(self, httpapifs, path, mode):
        self.httpapifs = httpapifs
        self.path = normpath(path)
        self.mode = mode
        self.closed = False
        self.file_size = None
        if 'r' in mode or 'a' in mode:
            self.file_size = httpapifs.getsize(path)

    def read(self):
        get = {
                'cmd':'view'
                ,'file':self.path
            }
        f = self.httpapifs.urlopen({}, get = get)
        return f.read()
        
    def write(self, data):
        get = {
                'cmd':'upload'
            }
        headers = {
            'X_FILE_NAME':self.path
        }
        f = self.httpapifs.urlopen(data, get = get, headers = headers)
        #r = urlopen( Request(self.httpapifs.root_url + '?' + urlencode(get), data, headers ) )

    def close(self):
        self.closed = True        

 
class HTTPAPIFS(FS):
    
    """Uses the HTTP FileBrowser API to read and write to remote filesystems via HTTP"""
    
    _meta = { 'network' : True,
              'virtual': False,
              'read_only' : False,
              'unicode_paths' : True,
              'case_insensitive_paths' : False,
              'atomic.move' : True,
              'atomic.copy' : True,              
              'atomic.makedir' : True,
              'atomic.rename' : True,
              'atomic.setcontents' : True,
              'file.read_and_write' : False,
              }
              
    def __init__(self, url, username = None, password = None):        
        self.root_url = url
        self.username = username
        self.password = password
        self.cache_paths = {}
       
    def urlopen( self, data, get = {}, headers = {}):
        if self.username and self.username!='' and self.password and self.password!='':
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, self.root_url, self.username, self.password)
            authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)
        
        get = get and ('?'+urlencode(get)) or ""
        r = urllib2.urlopen( urllib2.Request(self.root_url + get, urlencode(data), headers ) )
        return r
        
    def cacheReset(self):
        self.cache_paths = {}
        
 
    def getsize(self, path):
        item = self.__getNodeInfo( path )
        return item.get('size',0)

    def _check_path(self, path):
        path = normpath(path)
        base, fname = pathsplit(abspath(path))
        
        dirlist = self._readdir(base)
        if fname and fname not in dirlist:
            raise ResourceNotFoundError(path)
        return dirlist, fname

    def getinfo(self, path, overrideCache = False):
        node = self.__getNodeInfo(path, overrideCache = overrideCache)
        node['modified_time'] = datetime.datetime.fromtimestamp(node['modified_time'])
        node['created_time'] = node['modified_time']
        return node

        
    def open(self, path, mode="r"):

        path = normpath(path)
        mode = mode.lower()        
        if self.isdir(path):
            raise ResourceInvalidError(path)        
        if 'a' in mode or '+' in mode:
            raise UnsupportedError('write')
            
        if 'r' in mode:
            if not self.isfile(path):
                raise ResourceNotFoundError(path)

        f = _HTTPAPIFSFile(self, normpath(path), mode) 
        return f 
 
    
    def exists(self, path):
        return self.isfile(path) or self.isdir(path)
    
    def isdir(self, path):
        item = self.__getNodeInfo( path )
        if item:
            # attribute may not be present in the JSON for dirs
            return (item.get('leaf') != True)
        else:
            return False

    
    def isfile(self, path):
        item = self.__getNodeInfo( path )
        if item:
            return (item.get('leaf') == True)
        else:
            return False

    def makedir(self, path, recursive=False, allow_recreate=False):
        path = normpath(path)
        if path in ('', '/'):
            return
        post = {
            'cmd':'newdir'
            ,'dir':path
        }

        f = self.urlopen( post )
        d  = simplejson.load( f )
        f.close()
        return (d['success']=='true')
        
    def rename(self, src, dst, overwrite=False, chunk_size=16384):
        if not overwrite and self.exists(dst):
            raise DestinationExistsError(dst)
        post = {
            'cmd':'rename'
            ,'oldname':src
            ,'newname':dst
        }
        f = self.urlopen( post )
        d  = simplejson.load( f )
        f.close()
        
        self.refreshDirCache( src )
        self.refreshDirCache( dst )
         
        return (d['success']=='true')

    def refreshDirCache(self, path):
        (root1, file) = self.__getBasePath( path )
        # reload cache for dir
        self.listdir(root1, overrideCache=True)

    def removedir(self, path):        
        if not self.isdir(path):
            raise ResourceInvalidError(path)
        return self.remove( path, False )
        
    def remove(self, path, checkFile = True):        
        if not self.exists(path):
            raise ResourceNotFoundError(path)
        if checkFile and not self.isfile(path):
            raise ResourceInvalidError(path)
        
        post = {
            'cmd':'delete'
            ,'file':path
        }
        f = self.urlopen( post )
        d  = simplejson.load( f )
        f.close()
        self.refreshDirCache( path )
        return (d['success']=='true')
        
    def __getBasePath(self, path):
        parts = path.split('/')
        root = './'
        file = path
        if len(parts)>1:
            root = '/'.join(parts[:-1])
            file = parts[-1]
        return root, file
        
    def __getNodeInfo(self, path, overrideCache = False):
        # check if file exists in cached data or fecth target dir
        (root, file) = self.__getBasePath( path )
         
        cache = self.cache_paths.get( root )
        # check if in cache
        item = None
        if cache and not overrideCache:
            item = [item for item in cache if item['text']==file] or None
            if item: 
                item = item[0]
        else:
            # fetch listdir in cache then restart
            res = self.listdir( root )
            if res:
                item = self.__getNodeInfo( path )
        return item
            
    def close(self):
        # for cacheFS   
        pass
        
    def listdir(self, path="./",
                      wildcard=None,
                      full=False,
                      absolute=False,
                      dirs_only=False,
                      files_only=False,
                      overrideCache=False
                      ):

        cache = self.cache_paths.get(path)
        if cache and not overrideCache:
            list = [a['text'] for a in cache]
            return list
            
        post = {
            'cmd':'get'
            ,'path':path
        }
        print 'HTTP FETCH %s' % self.root_url, path, post
        f = self.urlopen( post )
        d  = simplejson.load( f )
        f.close()
        list = []
        if d:
            self.cache_paths[path] = d
            list = [a['text'] for a in d]
        
        return self._listdir_helper(path, list, wildcard, full, absolute, dirs_only, files_only)
