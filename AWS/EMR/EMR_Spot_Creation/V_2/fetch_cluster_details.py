def il(pkg):
    """
    Input:
        pkg - Package name you want to import
    Output:
        Install(If package is not installed already) and Import the package
    """
    import importlib
    import subprocess
    try:
        return importlib.import_module('%s' % (pkg))
    except:
        subprocess.call(['pip', 'install', '--user', pkg])
        return importlib.import_module('%s' % (pkg))
        
boto3 = il('boto3')
sys = il('sys')
time = il('time')
ast = il('ast')
json = il('json')
client = boto3.client('emr', region_name='us-east-1')

clus_id_dic = sys.argv[1]
keyname = sys.argv[2]

#print(clus_id_dic)
clus_id_dic = json.loads(str(clus_id_dic))
clus_id = clus_id_dic["ClusterId"]

idx=0
animation = "|/-\\"
print("\n")
while True:
    print("Initiating the cluster and an IP will be assigned shortly...."+animation[idx % len(animation)], end="\r")
    idx+=1
    try:
        time.sleep(0.1)
        clus_info = client.describe_cluster(ClusterId=clus_id)
        ip_ = clus_info['Cluster']['MasterPublicDnsName']
    except:
        continue
    break


tup = (keyname,ip_)

print("run the command 'ssh -i ~/%s.pem hadoop@%s'"%tup)
