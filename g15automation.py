import boto3
from g15_config import *
import traceback


def process_CRED(somecred):
    """
    Process pasted aws educate CLI credentials from labs.vocareum.com
    Note that this credential's validity is only 3 hours
    Return a list [aws_access_key_id,aws_secret_access_key,aws_session_token]
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


def create_security_group():
    global G15_VPC_ID
    global G15_SG_ID
    client_ec2 = g15session.client('ec2')
    vpc_response = client_ec2.describe_vpcs()
    G15_VPC_ID = vpc_response["Vpcs"][0]["VpcId"]
    # create security groups
    try:
        """initial all 4 secuurity groups first"""
        web_sg_res = client_ec2.create_security_group(GroupName=G15_SG_WEB,
                                                      Description=G15_SG_WEB_DESC,
                                                      VpcId=G15_VPC_ID)
        G15_SG_ID.web = web_sg_res['GroupId']  # WEB

        mongo_sg_res = client_ec2.create_security_group(GroupName=G15_SG_MONGO,
                                                        Description=G15_SG_MONGO_DESC,
                                                        VpcId=G15_VPC_ID)
        G15_SG_ID.mongo = mongo_sg_res['GroupId']  # MONGODB

        mysql_sg_res = client_ec2.create_security_group(GroupName=G15_SG_MYSQL,
                                                        Description=G15_SG_MYSQL_DESC,
                                                        VpcId=G15_VPC_ID)
        G15_SG_ID.mysql = mysql_sg_res['GroupId']  # MYSQL

        web_hadoop_res = client_ec2.create_security_group(GroupName=G15_SG_HADOOP,
                                                          Description=G15_SG_HADOOP_DESC,
                                                          VpcId=G15_VPC_ID)
        G15_SG_ID.hadoop = web_hadoop_res['GroupId']  # HADOOP
        """Add IP permissions"""
        #########################################
        # WEB security group
        res = client_ec2.authorize_security_group_ingress(GroupId=G15_SG_ID.web,
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
        res = client_ec2.authorize_security_group_ingress(GroupId=G15_SG_ID.mongo,
                                                          IpPermissions=[
                                                              {'IpProtocol': 'tcp',
                                                               'FromPort': 27017,
                                                               'ToPort': 27017,
                                                               'UserIdGroupPairs': [
                                                                   {
                                                                       'Description': 'intranet connectivity',
                                                                       'GroupId': G15_SG_ID.web,
                                                                   },
                                                               ], },
                                                          ])
        #########################################

    except Exception as e:
        traceback.print_exc()


# initialize session and ec2
g15session = get_aws_session()
g15ec2 = g15session.resource('ec2')

# initialized ssh key
create_ssh_key()

# initialize VPC and security groups
create_security_group()

# create MySQL instance
g15_ins_mysql = g15ec2.create_instances(ImageId=IMAGEID, MinCount=1, MaxCount=1,
                                        InstanceType='t2.micro', KeyName=G15_SSH_KEY)
print(g15_ins_mysql)
