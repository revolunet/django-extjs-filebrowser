django-extjs-explorer
=====================

django pluggable app with ExtJs based explorer like to browse, manage, upload and download files to many filesystems.

The django backend uses PyFilesystem so you can read/write to differents datasources and copy files across differents servers or amazon s3 buckets.

The example django app is located at [djangoproject/apps/django_extjs_filebrowser][10]

Comments welcome at [contact@revolunet.com][8]
 
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

 * git clone
 * git submodule update
 * configure djangoproject/local_settings.py and djangoproject/apps/django_extjs_filebrowser/settings.py from the samples
 * start python djangoproject/scripts/manage.py runserver
 * point a decent browser to http://127.0.0.1:8000
 * manage your files
 



  [1]: http://www.djangoproject.com
  [2]: http://code.google.com/p/pyfilesystem/
  [3]: http://www.sencha.com
  [4]: http://filetree.extjs.eu/
  [5]: https://github.com/revolunet/Ext.ux.filebrowser
  [6]: https://github.com/revolunet/Ext.ux.upload
  [7]: http://www.swfupload.org
  [8]: mailto:contact@revolunet.com
  [9]: https://github.com/revolunet/django-extjs-filebrowser/raw/master/example.jpg
  [10]: https://github.com/revolunet/django-extjs-filebrowser/tree/master/djangoproject/apps/django_extjs_filebrowser