from os import truncate
from pickle import NONE
import boto3
from g15_config import *
import traceback
import os
import pickle
import time


def process_CRED(somecred):
    """
    Process pasted aws educate CLI credentials from labs.vocareum.com
    Note that this credential's validity is only 3 hours
    Return a list [aws_access_key_id,aws_secret_access_key,aws_session_token]g15ec2
    """
    temp = somecred.split('\n')
    result = []
    result.append(temp[0][temp[0].index('=')+1:])
    result.append(temp[1][temp[1].index('=')+1:])
    result.append(temp[2][temp[2].index('=')+1:])
    return result


def get_aws_session():
    g15credentials = process_CRED(CRED)
    temp_session = boto3.session.Session(aws_access_key_id=g15credentials[0],
                                         aws_secret_access_key=g15credentials[1],
                                         aws_session_token=g15credentials[2],
                                         region_name='us-east-1')
    return temp_session


def create_ssh_key():
    try:
        g15_ssh_key_res = g15ec2.create_key_pair(KeyName=G15_SSH_KEY)
    except Exception as e:
        g15_ssh_key_res = e
    return g15_ssh_key_res


def store_instance_ip(instance_id, instance_name):
    filters = [
        {'Name': 'instance-id', 'Values': [instance_id]}
    ]
    while True:
        response = list(g15ec2.instances.filter(Filters=filters))
        try:
            pub = response[0].public_ip_address
            pri = response[0].public_ip_address
            if pub is not None:
                G15_INSTANCE[instance_name] = {'id': instance_id,
                                               'public_ip': pub,
                                               'private_ip': pri}
                break
        except:
            pass
        time.sleep(2)


def select_instance_type(ins_name):
    global G15_SELECT_ASK
    if G15_SELECT_ASK == '':
        # initial ask string
        temp = f'Please select which instance type for {ins_name} (default t2.medium):\n'
        for k, v in G15_INSTANCE_TYPE.items():
            temp += f'({k}) {v}\t'
        temp += '\nPlease input an integer index:'
        G15_SELECT_ASK = temp
    while True:
        selection = input(G15_SELECT_ASK)
        try:
            if selection == '':
                selection = 3
                break
            selection = int(selection)
            break
        except:
            print('Please inout an integer.')
    return G15_INSTANCE_TYPE[selection]


def create_security_group():
    global G15_VPC_ID
    global G15_SG_ID
    vpc_response = g15ec2client.describe_vpcs()
    G15_VPC_ID = vpc_response["Vpcs"][0]["VpcId"]
    # test
    if os.path.exists('sg_ids'):
        G15_SG_ID = pickle.load(open('sg_ids', 'rb'))
    ##
    # create security groups
    try:
        """initial all 4 secuurity groups first"""
        web_sg_res = g15ec2client.create_security_group(GroupName=G15_SG_WEB,
                                                        Description=G15_SG_WEB_DESC,
                                                        VpcId=G15_VPC_ID)
        G15_SG_ID.web = web_sg_res['GroupId']  # WEB

        mongo_sg_res = g15ec2client.create_security_group(GroupName=G15_SG_MONGO,
                                                          Description=G15_SG_MONGO_DESC,
                                                          VpcId=G15_VPC_ID)
        G15_SG_ID.mongo = mongo_sg_res['GroupId']  # MONGODB

        mysql_sg_res = g15ec2client.create_security_group(GroupName=G15_SG_MYSQL,
                                                          Description=G15_SG_MYSQL_DESC,
                                                          VpcId=G15_VPC_ID)
        G15_SG_ID.mysql = mysql_sg_res['GroupId']  # MYSQL

        web_hadoop_res = g15ec2client.create_security_group(GroupName=G15_SG_HADOOP,
                                                            Description=G15_SG_HADOOP_DESC,
                                                            VpcId=G15_VPC_ID)
        G15_SG_ID.hadoop = web_hadoop_res['GroupId']  # HADOOP
        """Add IP permissions"""
        #########################################
        # WEB security group
        res = g15ec2client.authorize_security_group_ingress(GroupId=G15_SG_ID.web,
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
        #########################################
        # mongodb security group
        res = g15ec2client.authorize_security_group_ingress(GroupId=G15_SG_ID.mongo,
                                                            IpPermissions=[
                                                                {'IpProtocol': 'tcp',
                                                                 'FromPort': 27017,
                                                                 'ToPort': 27017,
                                                                 'UserIdGroupPairs': [
                                                                     {
                                                                         'Description': 'intranet connectivity from mongo to web',
                                                                         'GroupId': G15_SG_ID.web,
                                                                     },
                                                                     {
                                                                         'Description': 'intranet connectivity from mongo to hadoop',
                                                                         'GroupId': G15_SG_ID.hadoop,
                                                                     },
                                                                 ], },
                                                            ])
        #########################################
        # mysql security group
        res = g15ec2client.authorize_security_group_ingress(GroupId=G15_SG_ID.mysql,
                                                            IpPermissions=[
                                                                {'IpProtocol': 'tcp',
                                                                 'FromPort': 3306,
                                                                 'ToPort': 3306,
                                                                 'UserIdGroupPairs': [
                                                                     {
                                                                         'Description': 'intranet connectivity from mysql to web',
                                                                         'GroupId': G15_SG_ID.web,
                                                                     },
                                                                     {
                                                                         'Description': 'intranet connectivity from mysql to hadoop',
                                                                         'GroupId': G15_SG_ID.hadoop,
                                                                     },
                                                                 ], },
                                                            ])
        #########################################
        # hadoop security group
        res = g15ec2client.authorize_security_group_ingress(GroupId=G15_SG_ID.hadoop,
                                                            IpPermissions=[
                                                                {'IpProtocol': 'tcp',
                                                                 'FromPort': 9000,
                                                                 'ToPort': 9000,
                                                                 'UserIdGroupPairs': [
                                                                     {
                                                                         'Description': 'intranet connectivity in hadoop cluster',
                                                                         'GroupId': G15_SG_ID.hadoop,
                                                                     },
                                                                 ], },
                                                                {'IpProtocol': 'tcp',
                                                                    'FromPort': 9866,
                                                                    'ToPort': 9866,
                                                                    'UserIdGroupPairs': [
                                                                        {
                                                                            'Description': 'intranet connectivity in hadoop cluster',
                                                                            'GroupId': G15_SG_ID.hadoop,
                                                                        },
                                                                    ], },
                                                            ])
        #########################################
        fp = open('sg_ids', 'wb')
        pickle.dump(G15_SG_ID, fp)
        fp.close()
    except Exception as e:
        traceback.print_exc()


# initialize session and ec2
g15session = get_aws_session()
g15ec2 = g15session.resource('ec2')
g15ec2client = g15session.client('ec2')

# initialized ssh key
create_ssh_key()

# initialize VPC and security groups
create_security_group()

# create WEB instance
webtype = select_instance_type("WEB")
g15_ins_web = g15ec2.create_instances(ImageId=IMAGEID, MinCount=1, MaxCount=1,
                                      InstanceType=webtype, KeyName=G15_SSH_KEY,
                                      SecurityGroupIds=[G15_SG_ID.web])
# create MySQL instance
mysqltype = select_instance_type("MySQL")
g15_ins_mysql = g15ec2.create_instances(ImageId=IMAGEID, MinCount=1, MaxCount=1,
                                        InstanceType=mysqltype, KeyName=G15_SSH_KEY,
                                        SecurityGroupIds=[G15_SG_ID.mysql])
# create MongoDB instance
mongotype = select_instance_type("MongoDB")
g15_ins_mongo = g15ec2.create_instances(ImageId=IMAGEID, MinCount=1, MaxCount=1,
                                        InstanceType=mongotype, KeyName=G15_SSH_KEY,
                                        SecurityGroupIds=[G15_SG_ID.mongo])
# print(g15_ins_mysql[0].id)
# store_instance_ip(g15_ins_mysql[0].id,'mysql')

store_instance_ip(g15_ins_mysql[0].id,'mysql')
store_instance_ip(g15_ins_mysql[0].id,'mysql')
store_instance_ip(g15_ins_mysql[0].id,'mysql')