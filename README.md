django-extjs-filebrowser
========================

There is a wroking demo here : [http://filebrowser.demo.revolunet.com][15]

django pluggable app with ExtJs based explorer like to browse, manage, upload and download files to many filesystems.

The django backend uses PyFilesystem so you can read/write to differents datasources and copy files across differents servers or amazon s3 buckets.

The  [master branch][12] is the reusable app itself and you have a django-example branch with a [working django project][13]

Code is released under [BSD licence][14] and your comments are welcome at [contact@revolunet.com][8]
 
![screenshot image viewer][9]

**Features :**

 * Browse directory tree
 * FileSystems : Locals / UNC paths / Amazon S3 / FTP / SFTP
 * HTML5 Drag&Drop Upload + SWFUpload failover
 * Preview and download files
 * copy files across diffferent filesystems
 
 
**Technologies used :**

 * [Django for the server side][1]
 * [PyFileSystem for file access][2]
 * [ExtJs][3] for GUI, with [Saki's FileTreePanel][4], and revolunet [Ext.ux.FileBrowser][5]
 * HTML5 Drag&Drop + Upload with revolunet [Ext.ux.upload][6]
 * [SWFupload][7] flash SWF upload
 
 
**Installation**

 * This is how to install the full django-example :
 * git clone [git@github.com:revolunet/django-extjs-filebrowser.git][11]
 * git fetch
 * git branch --track django-example origin/django-example
 * git checkout django-example
 * git submodule update --init
 * cd djangoproject/apps/django_extjs_filebrowser
 * git submodule update --init
 * configure djangoproject/local_settings.py and djangoproject/apps/django_extjs_filebrowser/settings.py from the samples
 * set EXTJS_PATH and DJANGO_SOURCE variables to point to these libs. (licence problem for ExtJs)
 * start python djangoproject/scripts/manage.py runserver
 * point a decent browser to http://127.0.0.1:8000
 * manage your files
 
**Todo**

 * static redirections
 * github like ajax history
 * icons from filetypes
 * add PHP proxy example
 * add FS : Google docs, drop.io...
 * drag from UI to desktop ?
 * handle move/copy


  [1]: http://www.djangoproject.com
  [2]: http://code.google.com/p/pyfilesystem/
  [3]: http://www.sencha.com
  [4]: http://filetree.extjs.eu/
  [5]: https://github.com/revolunet/Ext.ux.filebrowser
  [6]: https://github.com/revolunet/Ext.ux.upload
  [7]: http://www.swfupload.org
  [8]: mailto:contact@revolunet.com
  [9]: https://github.com/revolunet/django-extjs-filebrowser/raw/django-example/example.jpg
  [10]: https://github.com/revolunet/django-extjs-filebrowser/tree/master/djangoproject/apps/django_extjs_filebrowser
  [11]: git@github.com:revolunet/django-extjs-filebrowser.git
  [12]: https://github.com/revolunet/django-extjs-filebrowser/tree/master
  [13]: https://github.com/revolunet/django-extjs-filebrowser/tree/django-example
  [14]: https://github.com/revolunet/django-extjs-filebrowser/tree/master/licence.txt
  [15]: http://filebrowser.demo.revolunet.com