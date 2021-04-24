echo Give a name to your cluster
read name
echo "Give an valid instance type you want for Master(like m4/m10/r4/c3)"
read master_instancetype
echo "Give a valid size for your Master instance (like 4/8/10/16)"
read master_instancesize
echo "How many Master instances do you need"
read master_instancecount
echo "Give an valid instance type you want for Nodes(like m4/m10/r4/c3 type)"
read slave_instancetype
echo "Give a valid size for your Node instance (like 4/8/10/16)"
read slave_instancesize
echo "How many nodes do you need"
read slave_instancecount
echo "Part of AutoScaling, Minimum how many instances do you need"
read min_slave_count
echo "Part of AutoScaling, Maximum how many instances do you need"
read max_slave_count
echo "Give your pem key name"
read key

res=`aws emr create-cluster --name $name --applications Name=Hadoop Name=Hive Name=Spark Name=Pig Name=Livy --release-label emr-5.29.0 --service-role EMR_DefaultRole --ec2-attributes InstanceProfile=EMR_EC2_DefaultRole,KeyName=$key,SubnetId=subnet-f7eed0df --auto-scaling-role EMR_AutoScaling_DefaultRole --instance-groups Name=MyMasterIG,BidPrice=2,InstanceGroupType=MASTER,InstanceType="${master_instancetype}.${master_instancesize}xlarge",InstanceCount=$master_instancecount 'Name=MyCoreIG,BidPrice=2,InstanceGroupType=CORE,InstanceType='"${slave_instancetype}.${slave_instancesize}xlarge"',InstanceCount='$slave_instancecount',AutoScalingPolicy={Constraints={MinCapacity='$min_slave_count',MaxCapacity='$max_slave_count'},Rules=[{Name=Default-scale-out,Description=Replicates the default scale-out rule in the console.,Action={SimpleScalingPolicyConfiguration={AdjustmentType=CHANGE_IN_CAPACITY,ScalingAdjustment=1,CoolDown=300}},Trigger={CloudWatchAlarmDefinition={ComparisonOperator=GREATER_THAN_OR_EQUAL,EvaluationPeriods=2,MetricName=YARNMemoryAvailablePercentage,Namespace=AWS/ElasticMapReduce,Period=300,Statistic=AVERAGE,Threshold=80,Unit=PERCENT,Dimensions=[{Key=JobFlowId,Value="${emr.clusterId}"}]}}},{Name=Default-scale-in,Description=Replicates the default scale-in rule in the console.,Action={SimpleScalingPolicyConfiguration={AdjustmentType=CHANGE_IN_CAPACITY,ScalingAdjustment=-1,CoolDown=300}},Trigger={CloudWatchAlarmDefinition={ComparisonOperator=LESS_THAN_OR_EQUAL,EvaluationPeriods=2,MetricName=YARNMemoryAvailablePercentage,Namespace=AWS/ElasticMapReduce,Period=300,Statistic=AVERAGE,Threshold=20,Unit=PERCENT,Dimensions=[{Key=JobFlowId,Value="${emr.clusterId}"}]}}}]}'`

#echo $res
python fetch_cluster_details.py "$res" $key
