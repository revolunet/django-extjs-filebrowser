

from fs.osfs import OSFS
from fs.s3fs import S3FS

 
    
AWS_ACCESS_KEY_ID  = 'AKIAJNQ4IARVJKRBCYAQ'
AWS_SECRET_ACCESS_KEY ='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'



sources = {
    'testfolder':{
        'cls':OSFS
        ,'params':{
            'root_path':r'C:\Q3Ademo'
            #,'encoding':
        }
    }
    ,'s3test':{
        'cls':S3FS
        ,'params':{
            'bucket':'bucket21'
            ,'aws_access_key':AWS_ACCESS_KEY_ID
            ,'aws_secret_key':AWS_SECRET_ACCESS_KEY
            #,'prefix':AWS_ACCESS_KEY_ID.lower()
        }
    }
    
   
}

 