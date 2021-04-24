#!/usr/bin/env python
# coding: utf-8
# author: atanu maity
# instruction to use: You need to ssh from a instance where you will have credentials already set up and you need to have instance/emr creation permission in resepct of your credentials. 
#######################################################################################################################

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

m_type_ = input("Give an valid instance type you want for Master(like m4/m10/r4/c3 type): ")
m_size = input("\nGive a valid size for your Master instance (like 4/8/10/16): ")
m_count = input("\nHow many Master instances do you need: ")
s_type_ = input("\nGive an valid instance type you want for Nodes(like m4/m10/r4/c3 type): ")
s_size = input("\nGive a valid size for your Node instance (like 4/8/10/16): ")
s_count = input("\nHow many nodes do you need: ")
emr_name = input("\nGive a name to your EMR (like 'data_extraction_instance'): ")
keyname = input("\nPass the pem key name which should be used to login into the instance (eg. 'amp-key'): ")
#ebs_volume = input("\nhow much EBS volume do you want (like 250/400): ")
minCap = input('\nPart of AutoScaling, Minimum how many instances do you need: ')
maxCap = input('\nPart of AutoScaling, Maximum how many instances do you need: ')



client = boto3.client('emr', region_name='us-east-1')

response = client.run_job_flow(
    Name=emr_name,
    ReleaseLabel='emr-5.23.0',
    AutoScalingRole='EMR_AutoScaling_DefaultRole',
    Instances={
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False,
        'Ec2SubnetId': 'subnet-f7eed0df',
        'Ec2KeyName': keyname,
        'InstanceGroups': [{"Name": "MyCoreIG","Market": "SPOT",'InstanceRole':'CORE','InstanceCount':int(s_count),'InstanceType':'%s.%sxlarge'%(s_type_,s_size),'AutoScalingPolicy':{
        'Constraints': {
            'MinCapacity': int(minCap),
            'MaxCapacity': int(maxCap)
        },
        'Rules': [
            {
                'Name': 'scaling_out',
                'Action': {
                    'SimpleScalingPolicyConfiguration': {
                        'AdjustmentType': 'EXACT_CAPACITY',
                        'ScalingAdjustment': 1,
                        'CoolDown': 100
                    }
                },
                'Trigger': {
                    'CloudWatchAlarmDefinition': {
                        'ComparisonOperator': 'GREATER_THAN_OR_EQUAL',
                        'MetricName': 'YARNMemoryAvailablePercentage',
                        'Period': 300,
                        'Threshold': 80,
                        'Unit':'PERCENT',
                        'EvaluationPeriods':2,
                        "Statistic": "AVERAGE",
                        "Namespace": "AWS/ElasticMapReduce",
                        "Dimensions":[
             {
               "Key" : "JobFlowId",
               "Value" : "${emr.clusterId}"
             }
          ]
                    }
                }
            },
            
            {
                'Name': 'scaling_in',
                'Action': {
                    'SimpleScalingPolicyConfiguration': {
                        'AdjustmentType': 'EXACT_CAPACITY',
                        'ScalingAdjustment': -1,
                        'CoolDown': 100
                    }
                },
                'Trigger': {
                    'CloudWatchAlarmDefinition': {
                        'ComparisonOperator': 'LESS_THAN_OR_EQUAL',
                        'MetricName': 'YARNMemoryAvailablePercentage',
                        'Period': 300,
                        'Threshold': 20,
                        'Unit':'PERCENT',
                        'EvaluationPeriods':2,
                        "Statistic": "AVERAGE",
                        "Namespace": "AWS/ElasticMapReduce",
                        "Dimensions":[
             {
               "Key" : "JobFlowId",
               "Value" : "${emr.clusterId}"
             }
          ]
                    }
                }
                
            }
        ]
    }},{'InstanceRole':'MASTER',"Market": "SPOT",'InstanceCount':int(m_count),'InstanceType':'%s.%sxlarge'%(m_type_,m_size),"Name": "MyMasterIG"}]
    },
    VisibleToAllUsers=True,
    JobFlowRole='EMR_EC2_DefaultRole',
    ServiceRole='EMR_DefaultRole',
)

clus_id = response['JobFlowId']
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

print("run the command 'ssh -i %s.pem hadoop@%s'"%tup)
