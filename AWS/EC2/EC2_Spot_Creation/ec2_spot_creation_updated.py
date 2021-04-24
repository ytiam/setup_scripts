#!/usr/bin/env python
# coding: utf-8
# author: atanu maity

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


def il_all(pkg_lst=[]):
    """
    Input:
        pkg_lst - A list of packages you want to import, if passed blank only the default packages will be imported

    Output:
        A list of all packages imported
    """
    pkg_lst_default = ['os']
    for l in pkg_lst:
        pkg_lst_default.append(l)
    return [il(j) for j in pkg_lst_default]

def retrive_ec2_info(id_):
    """
    A tool for retrieving basic information from the running EC2 instances.
    """
    from collections import defaultdict
    # information for all running instances
    running_instances = ec2.instances.filter(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['running']}])

    ec2info = dict()
    for instance in running_instances:
        if instance.id == id_:
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                    name = tag['Value']
            # Add instance info to a dictionary         
            ec2info[instance.id] = {
                'Name': name,
                'Type': instance.instance_type,
                'State': instance.state['Name'],
                'Private IP': instance.private_ip_address,
                'Public IP': instance.public_ip_address,
                'Launch Time': instance.launch_time
                }

    attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
    for instance_id, instance in ec2info.items():
        for key in attributes:
            print("{0}: {1}".format(key, instance[key]))
        print("------")
    
    return ec2info

boto3 = il('boto3')
sys = il('sys')
time = il('time')

type_ = input("Give an valid instance type you want(like m4/m10/r4/c3 type): ")
size = input("\nGive a valid size for your instance (like 4/8/10/16): ")
instance_name = input("\nGive a name to your instance (like 'data_extraction_instance'): ")
project_val = input("\nGive the project name, you are creating this instance for (like 'amp'): ")
image_id = input("\nGive the aws image id which you want to set your instance with (eg. 'ami-ea542890'): ")
keyname = input("\nPass the pem key name which should be used to login into the instance (eg. 'amp-key'): ")
maxprice = input("\nGive the max price you will allow for this spot instance (like 2/4/8). The unit is in $: ")
ebs_volume = input("\nhow much EBS volume do you want (like 250/400): ")

ec2 = boto3.resource('ec2',region_name='us-east-1')

instances = ec2.create_instances(
     ImageId=image_id, #'ami-ea542890'
     MinCount=1,
     MaxCount=1,
     InstanceType='%s.%sxlarge'%(type_,size),
     KeyName=keyname,
     EbsOptimized= True,
     NetworkInterfaces= [ { 'AssociatePublicIpAddress': False,'DeviceIndex': 0,'SubnetId':'subnet-f7eed0df',
                          'Groups':['sg-c4f521b6']}],
     InstanceMarketOptions={
        'MarketType': 'spot',
        'SpotOptions': {
            'MaxPrice': maxprice, #'4'
            'SpotInstanceType': 'one-time'}},
     BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {

                'DeleteOnTermination': True,
                'VolumeSize': int(ebs_volume), #250
                'VolumeType': 'gp2'
            },
        },
    ],
)

iid = instances[0].id

ec2.create_tags(
    Resources = [iid],
    Tags = [{'Key': 'project', 'Value': project_val}
            ,{'Key':'Name','Value':instance_name}]
   )

time.sleep(20)

ec2_info = retrive_ec2_info(iid)

private_ip = ec2_info[iid]['Private IP']

tup = (keyname,private_ip,instance_name)

print('******************************')
print('run the command "ssh -i %s ubuntu@%s" to login into the %s instance'%tup)