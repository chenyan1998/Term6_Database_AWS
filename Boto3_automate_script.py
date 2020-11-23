import boto3
import botocore
from botocore.exceptions import ClientError
import time
session=boto3.session.Session(profile_name="default")

ec2 = session.client('ec2')
ec2_re=session.resource(service_name="ec2")

#Function creating a security group for Mysql instance
response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
def create_sg_Mysql_instance():
    try:
        response = ec2.create_security_group(GroupName='Mysql instance security group',
                                            Description='security group for Mysql instance',
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)    

#Function creating a security group for Mongodb instance
def create_sg_Mongodb_instance():
    try:
        response = ec2.create_security_group(GroupName='Mongodb instance security group',
                                            Description='security group for Mongodb instance',
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)

#Function creating a security group for Frontend instance
def create_sg_Frontend_instance():
    try:
        response = ec2.create_security_group(GroupName='Frontend instance security group',
                                            Description='security group for Frontend instance',
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)

#If security group for Mysql, Mongodb or Frontend not exists, create them
try:
    response = ec2.describe_security_groups(GroupNames=['Mysql instance security group'])
    print('security group Mysql instance exists')
except:
    create_sg_Mysql_instance()
    print("security group for Mysql instance has just been created")

try:
    response = ec2.describe_security_groups(GroupNames=['Mongodb instance security group'])
    print('security group Mongodb instance exists')    
except:
    create_sg_Mongodb_instance()
    print("security group for Mongodb instance has just been created")

try:
    response = ec2.describe_security_groups(GroupNames=['Frontend instance security group'])
    print('security group Frontend instance exists')    
except:
    create_sg_Frontend_instance()
    print("security group for Frontend instance has just been created")

#Generate key pair for three instances
key_not_found = True
keyPairs = ec2.describe_key_pairs()
for key in keyPairs.get('KeyPairs'):
    if key.get('KeyName') == 'group15_key':
        key_not_found = False
        print("key-pair: group15_key exists.")
        break
if key_not_found:
    print("Generating a key pair for EC2 instances")
    key_response = ec2.create_key_pair(KeyName='group15_key')
    print("key has been generated")

#Create three instances for Mysql, Mongodb and Frontend individually
Test_Mysql_Instance=ec2.run_instances(
    MaxCount=1,
    MinCount=1,
    ImageId='ami-0f82752aa17ff8f5d',
    InstanceType='t1.micro',
    KeyName='group15_key',
    SecurityGroups=['Mysql instance security group'],
    TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'name','Value': 'Mysql instance'},]}]
)
print("Mysql instance has been created")

Test_Mongodb_Instance=ec2.run_instances(
    MaxCount=1,
    MinCount=1,
    ImageId='ami-0f82752aa17ff8f5d',
    InstanceType='t1.micro',
    KeyName='group15_key',
    SecurityGroups=['Mongodb instance security group'],
    TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'name','Value': 'Mongodb instance'},]}]
)
print("Mongodb instance has been created")

Test_Frontend_Instance=ec2.run_instances(
    MaxCount=1,
    MinCount=1,
    ImageId='ami-0f82752aa17ff8f5d',
    InstanceType='t1.micro',
    KeyName='group15_key',
    SecurityGroups=['Frontend instance security group'],
    TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'name','Value': 'Frontend instance'},]}]
)
print("Frontend instance has been created")
print("Wait for new instances to be ready")
time.sleep(60)

# Retrive public ips for three instances
running_instances=[]
public_ips={}
instances = ec2_re.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    running_instances.append(instance.id)
    public_ips[instance.tags[0]['Value']]=instance.public_ip_address
print('Instances IDs are ', running_instances)
print('Instances ips for group15 are',public_ips)


