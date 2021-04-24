#!/usr/bin/env python
# coding: utf-8
# Author: Atanu Maity

import boto3
import sys

instance_name = sys.argv[1]

ec2 = boto3.resource('ec2',region_name='us-east-1')

instances = ec2.create_instances(
     ImageId='ami-ea542890',
     MinCount=1,
     MaxCount=1,
     InstanceType='r4.4xlarge',
     KeyName='metlife-key-1',
     EbsOptimized= True,
     NetworkInterfaces= [ { 'AssociatePublicIpAddress': False,'DeviceIndex': 0,'SubnetId':'subnet-f7eed0df',
                          'Groups':['sg-c4f521b6']}],
     InstanceMarketOptions={
        'MarketType': 'spot',
        'SpotOptions': {
            'MaxPrice': '2',
            'SpotInstanceType': 'one-time'}},
     BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {

                'DeleteOnTermination': True,
                'VolumeSize': 160,
                'VolumeType': 'gp2'
            },
        },
    ],
)

iid = instances[0].id

ec2.create_tags(
    Resources = [iid],
    Tags = [{'Key': 'project', 'Value': 'metblue'}
            ,{'Key':'Name','Value':instance_name}]
   )



