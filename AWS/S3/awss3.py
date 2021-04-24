import boto3
import pandas as pd


def listBucket():
    s3 = boto3.resource('s3')


def changeBucketVersion(bucket_name,status=None):

    '''
        Enable or suspend bucket versioning
        
        Parameters:
            bucket_name (string):   name of the bucket
            status (string):        Enable | Suspend         
        
    '''

    s3 = boto3.resource('s3')
    versioning = s3.BucketVersioning(bucket)
    
    if status == None:
        return
    
    if status == 'Enable':
        # enable versioning
        print("Enable versioning of {}".format(bucket_name))
        versioning.enable()
        
    else:
        # disable versioning
        print("Suspend versioning of {}".format(bucket_name))
        versioning.suspend()


def checkBucketVersionStatus(bucket_name):

    '''
        Check the versioning status of bucket
        
        Parameters:
            bucket_name (string): name of the bucket        
        
    '''

    s3 = boto3.resource('s3')
    versioning = s3.BucketVersioning(bucket_name)
    print(versioning.status)


def getObjectVersions(bucket_name,prefix=None):
    
    '''
        Get the leatest and oldest version of object
        
        Parameters: 
            bucket_name (string): name of the bucket
            prefix (string): name of the folder
  
        Returns: 
            list,list: Return latest and the oldest version of objext
        
    '''

    s3_client = boto3.client('s3')
    
    if prefix == None:    
        resp = s3_client.list_object_versions(Bucket=bucket_name)
    else:
        resp = s3_client.list_object_versions(Prefix=prefix, Bucket=bucket_name)
    
    latest_version,older_version = [],[]

    
    ## DeleteMarkers is when there is only deleted version persited. 
    ## We excluded "DeleteMarkers" from the list of all versioned.
    allVersions = [*resp['Versions'], *resp.get('DeleteMarkers', [])]
    
    for obj in allVersions: 
        size          = obj.get('Size', 0)/1e6 # In MB
        isLatest      = obj['IsLatest']        
        lastModified  = obj['LastModified']    
        name          = obj['Key']             
        VersionId     = obj['VersionId']       
        
        #print("size ",str(size))              
        
        if obj['IsLatest'] == True:
            latest_version.append(obj)
        if obj['IsLatest'] == False:
            older_version.append(obj)

    return latest_version, older_version


def getObjectVersiongFormat(objects):

    '''
        Return the list of versionid and size of each unique object(file/folder)

        Parameters: 
            objects (dict): list of objects             
  
        Returns: 
            dict: return dict, with object name as key and list of tupple of versions & size of each unique object.

    '''

    o = {}
    for obj in objects:
        size          = obj.get('Size', 0)/1e3
        isLatest      = obj['IsLatest']        
        lastModified  = obj['LastModified']    
        name          = obj['Key']             
        VersionId     = obj['VersionId'] 
        key           = obj['Key']

        if key in  o.keys():
            o[key].append((VersionId,size))
        else:
            o[key] = [(VersionId,size)]
    
    return o


def deleteObjects(bucket,listOfObjects,isDelete = False):


    '''
        Delete object that does not has any marker 'Latest version'

        Parameters: 
            listOfObjects (list): list of objects to be deleted  

    '''
    s3_client = boto3.client('s3')

    print("Bucket: " + bucket)

    reply = isDelete

    if isDelete == True:
        reply = input('Do you want to delete the older version of object (yes/no): ').lower().strip()
        isDelete = True if reply == 'yes' else False

    totalSize = 0
    print("Objects to be deleted.....")

    print("*"*110)
    if isDelete == True: print('{:10s}{:10s}{:35s}{:70s}'.format("Deleted","Size","VersionID","Object"))
    else: print('{:10s}{:35s}{:70s}'.format("Size","VersionID","Object",))

    print("*"*110)

    for obj in listOfObjects:

        key       = obj['Key']
        versionid = obj['VersionId']
        size      = obj.get('Size', 0)/1e6
        totalSize = totalSize + size

        if   size <= 10**3:  size = str(round(size,0)) + " MB"
        elif size <= 10**6:  size = str(round(size/10**3,2)) + " GB"
        elif size <= 10**9:  size = str(round(size/10**6,2)) + " TB"


        if isDelete == True:
            print('{:10s}{:10s}{:35s}{:70s}'.format("Deleted",size,versionid,key))

            ## Uncomment to delete
            #s3_client.delete_object(Bucket=bucket, Key=obj['Key'], VersionId=obj['VersionId'])
        else:
            print('{:10s}{:35s}{:100s}'.format(size,versionid,key))
    print("*"*110)

    if   totalSize <= 10**3:  totalSize = str(round(totalSize,0)) + " MB"
    elif totalSize <= 10**6:  totalSize = str(round(totalSize/10**3,2)) + " GB"
    elif totalSize <= 10**9:  totalSize = str(round(totalSize/10**6,2)) + " TB"

    print("\n\nTotal file size of deleted object is {}".format(totalSize))


def getDataFrameOfObjectVersions(list_of_object,df=None):

	'''
		Get a dataframe of objects with key inmortaion that include object name, version id,
		last modified date, whether latest version or not, size of object etc.

		Parameters:
            listOfObjects (list): list of objects
            df ( pandas Dataframe): Pass existing dataframe to add the object version. If not pass, then it will be created.

        Returns:
			df (pandas dataframe) : Return dataframe with key information of object version


	'''

    if type(df) != pd.core.frame.DataFrame:
        df = pd.DataFrame()
        df['object']             = []
        df['versionID']          = []
        df['isLatest']           = []
        df['size']               = []
        df['last_modified_date'] = []



    for obj in list_of_object:
        object_name = obj['Key']
        versionID   = obj['VersionId']
        isLatest    = str(obj['IsLatest'])
        size        = obj.get('Size', 0)/1e6
        last_m_date = obj['LastModified']

        if   size <= 10**3:  size = str(round(size,0)) + " MB"
        elif size <= 10**6:  size = str(round(size/10**3,2)) + " GB"
        elif size <= 10**9:  size = str(round(size/10**6,2)) + " TB"

        df.loc[len(df)] = [object_name,versionID,isLatest,size,last_m_date]

    return df