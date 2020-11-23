import boto3
import botocore
from botocore.exceptions import ClientError
session=boto3.session.Session(profile_name="default")

ec2 = session.client('ec2')
ec2_re=session.resource(service_name="ec2")
waiter = ec2.get_waiter('instance_terminated')

#Checking What instances are running with group15_key and store their ids in a list
running_instances=[]
instances = ec2_re.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']},{'Name':'key-name',"Values":["group15_key"]}])
for instance in instances:
    running_instances.append(instance.id)
print('Instances running for group15 are',running_instances)

#Terminating instances based on instance id
print("Terminating group15 instances, please wait...")
ec2_re.instances.filter(InstanceIds=running_instances).terminate()
waiter.wait(InstanceIds=running_instances)  
print("group15 instances terminated")

#Get security groups names and ids and store in dictionary
sg_name_list=['Mysql instance security group','Mongodb instance security group', 'Frontend instance security group']
response = ec2.describe_security_groups(
    Filters=[
        dict(Name='group-name', Values=sg_name_list)
    ]
)

sg_names_ids={}
for i in range(len(response['SecurityGroups'])):
    group_name = response['SecurityGroups'][i]["GroupName"]
    group_id = response['SecurityGroups'][i]['GroupId']
    sg_names_ids[group_name]=group_id
print("Existing security groups are ",sg_names_ids)

#Delete all security groups
def delete_all_security_groups():    #security group to be deleted must not have any dependence on them
    for i in sg_names_ids:
        response = ec2.delete_security_group(GroupId=sg_names_ids[i])
        print('Security Group {} Is Deleted'.format(i))
delete_all_security_groups()

#Delete group15_key
response = ec2.delete_key_pair(KeyName='group15_key')
print(response)