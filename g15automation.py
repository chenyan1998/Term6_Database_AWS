import boto3
import traceback
import os
import pickle
import time
import paramiko
from io import StringIO
from multiprocessing import Pool
import zipfile
import logging


def instance_config(option):
    global G15_INSTANCE
    if option == 'store':
        fp = open('instance_config', 'wb')
        pickle.dump(G15_INSTANCE, fp)
        fp.close()
    elif option == 'load':
        G15_INSTANCE = pickle.load(open('instance_config', 'rb'))


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
    global G15_SSH_KEY_PEM
    global G15_SSH_KEY
    try:
        if os.path.exists(G15_SSH_KEY):
            G15_SSH_KEY_PEM = pickle.load(open(G15_SSH_KEY, 'rb'))
            return G15_SSH_KEY_PEM
        else:
            g15_ssh_key_res = g15ec2.create_key_pair(KeyName=G15_SSH_KEY)
            G15_SSH_KEY_PEM = g15_ssh_key_res.key_material
            fp = open(G15_SSH_KEY, 'wb')
            pickle.dump(G15_SSH_KEY_PEM, fp)
            fp.close()
    except Exception as e:
        g15_ssh_key_res = e
    return g15_ssh_key_res


def store_instance_ip(instance_id, instance_name):
    global G15_INSTANCE
    filters = [
        {'Name': 'instance-id', 'Values': [instance_id]}
    ]
    while True:
        response = list(g15ec2.instances.filter(Filters=filters))
        try:
            pub = response[0].public_ip_address
            pri = response[0].private_ip_address
            if pub is not None:
                if 'node' in instance_name:
                    G15_INSTANCE[instance_name] = {'id': instance_id,
                                                   'public_ip': pub,
                                                   'private_ip': pri,
                                                   "hostname": f'com.g15.{instance_name}'}
                    break
                else:
                    G15_INSTANCE[instance_name] = {'id': instance_id,
                                                   'public_ip': pub,
                                                   'private_ip': pri,
                                                   }
                    break
        except:
            pass
        time.sleep(2)


def select_instance_type(ins_name):
    # TEST
    return G15_INSTANCE_TYPE[4]
    global G15_SELECT_ASK
    if G15_SELECT_ASK == '':
        # initial ask string
        temp = 'Please select which instance type for {} (default t2.medium):\n'
        for k, v in G15_INSTANCE_TYPE.items():
            temp += f'({k}) {v}\t'
        temp += '\nPlease input an integer index:'
        G15_SELECT_ASK = temp
    while True:
        selection = input(G15_SELECT_ASK.format(ins_name))
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
                                                                 'FromPort': 22,
                                                                 'ToPort': 22,
                                                                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
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
                                                                 'FromPort': 22,
                                                                 'ToPort': 22,
                                                                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
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
                                                                 'FromPort': 22,
                                                                 'ToPort': 22,
                                                                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
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
                                                                    'ToPort': 9867,
                                                                    'UserIdGroupPairs': [
                                                                        {
                                                                            'Description': 'intranet connectivity in hadoop cluster',
                                                                            'GroupId': G15_SG_ID.hadoop,
                                                                        },
                                                                    ], },
                                                                {'IpProtocol': 'tcp',
                                                                 'FromPort': 9864,
                                                                 'ToPort': 9864,
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


def send_shfile_exec(ip_addr, bash_file_path, files_to_upload, pem_string):
    while True:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            pem_k = paramiko.RSAKey.from_private_key(StringIO(pem_string))
            while True:
                try:
                    ssh_client.connect(
                        hostname=ip_addr, username='ubuntu', pkey=pem_k)
                    break
                except:
                    pass
            print(
                f'Start executing {bash_file_path.split("/")[-1]} upload files')
            sftp_client = ssh_client.open_sftp()
            sftp_client.put(
                bash_file_path, f'/home/ubuntu/{bash_file_path.split("/")[-1]}')
            for file_path in files_to_upload:
                sftp_client.put(
                    file_path, f'/home/ubuntu/{file_path.split("/")[-1]}')
            # other connections wait for Mongo to upload file
            if 'mongo' in bash_file_path.split("/")[-1]:
                sftp_client.get('home/ubuntu/.ssh/authorized_keys', 'g15pubkey')
                fp = open('closesftp', 'w')
                fp.close()
            while True:
                if os.path.exists("closesftp"):
                    time.sleep(2)
                    sftp_client.close()
                    break
                time.sleep(2)

            print(f'Start executing {bash_file_path.split("/")[-1]}')
            ssh_client.exec_command(
                f"sudo chmod +x /home/ubuntu/{bash_file_path.split('/')[-1]}", get_pty=True)
            stdin, stdout, stderr = ssh_client.exec_command(
                f'bash /home/ubuntu/{bash_file_path.split("/")[-1]}', get_pty=True)
            for line in iter(stdout.readline, ""):
                print(f"From {bash_file_path.split('/')[-1]} " + line, end="")
            ssh_client.close()
            print(f'done {bash_file_path.split("/")[-1]}')
            break
        except:
            traceback.print_exc()

# TEST
def hadoop_send_shfile_exec(ip_addr, bash_file_path, files_to_upload, pem_string, node):
    while True:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            pem_k = paramiko.RSAKey.from_private_key(StringIO(pem_string))
            while True:
                try:
                    ssh_client.connect(
                        hostname=ip_addr, username='ubuntu', pkey=pem_k)
                    break
                except:
                    pass
            print(
                f'Start executing {bash_file_path.split("/")[-1]} upload files')
            sftp_client = ssh_client.open_sftp()
            sftp_client.put(
                bash_file_path, f'/home/ubuntu/{bash_file_path.split("/")[-1]}')
            for file_path in files_to_upload:
                sftp_client.put(
                    file_path, f'/home/ubuntu/{file_path.split("/")[-1]}')
            while True:
                if os.path.exists("closesftp"):
                    time.sleep(2)
                    sftp_client.put(G15_SSH_PUBKEY,'/home/ubuntu/.ssh/authorized_keys')
                    sftp_client.put(G15_SSH_KEY,'/home/ubuntu/.ssh/id_rsa')
                    sftp_client.close()
                    break
                time.sleep(2)

            print(f'Start executing {bash_file_path.split("/")[-1]}')
            ssh_client.exec_command(
                f"sudo chmod +x /home/ubuntu/{bash_file_path.split('/')[-1]}", get_pty=True)
            stdin, stdout, stderr = ssh_client.exec_command(
                f'bash /home/ubuntu/{bash_file_path.split("/")[-1]}', get_pty=True)
            for line in iter(stdout.readline, ""):
                print(f"From {bash_file_path.split('/')[-1]} " + line, end="")
            ssh_client.close()
            print(f'done {bash_file_path.split("/")[-1]}')
            break
        except:
            traceback.print_exc()


def prepare_files(option):
    if option == 'web':
        # for web
        global G15_INSTANCE
        tarZip = zipfile.ZipFile('frontend.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk('frontend_template/'):
            for file_name in files:
                content = open(os.path.join(root, file_name),
                               'r', encoding="utf8").read()
                if file_name == 'config.py':
                    content = content.replace(
                        '[[1]]', G15_INSTANCE['mysql']["private_ip"])
                    content = content.replace(
                        '[[2]]', G15_INSTANCE['mongo']["private_ip"])
                elif file_name == 'main.js':
                    content = content.replace('[[1]]',
                                              f"http://{G15_INSTANCE['web']['public_ip']}/api")
                with open(f'frontend/{file_name}', 'w', encoding="utf8") as f:
                    f.write(content)
                tarZip.write(f'frontend/{file_name}')
        tarZip.close()
        return
    else:
        pass


def select_operation(option):
    if option == 'web':
        while True:
            _ = input("Setup WEB and Database?\n(1) Yes\t(2) No\n")
            try:
                if int(_) == 1:
                    return True
                elif int(_) == 2:
                    return False
            except:
                pass
    if option == 'hadoop':
        while True:
            _ = input("Setup Hadoop cluster?\n(1) Yes\t(2) No\n")
            try:
                if int(_) == 1:
                    while True:
                        __ = input(
                            "Please input how many datanodes you want to setup.\n")
                        try:
                            result = int(__)
                            if result == 0:
                                print("Invalid number")
                            else:
                                return result
                        except:
                            pass
                elif int(_) == 2:
                    return False
            except:
                pass


def initialize():
    # initialized ssh key
    create_ssh_key()

    # initialize VPC and security groups
    create_security_group()

    # logging
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def launch_web_db():
    # create MongoDB instance
    mongotype = select_instance_type("MongoDB")
    g15_ins_mongo = g15ec2.create_instances(ImageId=IMAGEID, MinCount=1, MaxCount=1,
                                            InstanceType=mongotype, KeyName=G15_SSH_KEY,
                                            SecurityGroupIds=[G15_SG_ID.mongo],
                                            TagSpecifications=[{'ResourceType': 'instance',
                                                                'Tags': [{'Key': 'Name', 'Value': 'MongoDB'}, ]}])
    # create WEB instance
    webtype = select_instance_type("WEB")
    g15_ins_web = g15ec2.create_instances(ImageId=IMAGEID, MinCount=1, MaxCount=1,
                                          InstanceType=webtype, KeyName=G15_SSH_KEY,
                                          SecurityGroupIds=[G15_SG_ID.web],
                                          TagSpecifications=[{'ResourceType': 'instance',
                                                              'Tags': [{'Key': 'Name', 'Value': 'WEB'}, ]}])
    # create MySQL instance
    mysqltype = select_instance_type("MySQL")
    g15_ins_mysql = g15ec2.create_instances(ImageId=IMAGEID, MinCount=1, MaxCount=1,
                                            InstanceType=mysqltype, KeyName=G15_SSH_KEY,
                                            SecurityGroupIds=[G15_SG_ID.mysql],
                                            TagSpecifications=[{'ResourceType': 'instance',
                                                                'Tags': [{'Key': 'Name', 'Value': 'MySQL'}, ]}])

    store_instance_ip(g15_ins_web[0].id, 'web')
    store_instance_ip(g15_ins_mysql[0].id, 'mysql')
    store_instance_ip(g15_ins_mongo[0].id, 'mongo')

    prepare_files('web')

    # executing commands
    try:
        os.remove('closesftp')
    except:
        pass
    p = Pool(3)   # two
    p.apply_async(send_shfile_exec, args=(
        G15_INSTANCE["mongo"]["public_ip"], 'mongo/mongo.bash', ["mongo/kindle_metadata_final.zip", "mongo/mongo_commands.js"], G15_SSH_KEY_PEM,))
    p.apply_async(send_shfile_exec, args=(
        G15_INSTANCE["mysql"]["public_ip"], 'mysql/mysql.bash', ["mysql/sql_commands.sql"], G15_SSH_KEY_PEM,))
    p.apply_async(send_shfile_exec, args=(
        G15_INSTANCE["web"]["public_ip"], 'frontend_template/web.bash', ["frontend.zip"], G15_SSH_KEY_PEM,))
    print('Wait for all processes done')
    p.close()
    p.join()

    # send_shfile_exec( G15_INSTANCE["mysql"]["public_ip"], 'Mysql_setup_script.bash', ["sql_commands.sql"], G15_SSH_KEY_PEM)
    print(f'You can visit http://{G15_INSTANCE["web"]["public_ip"]}')


def destroy_hadoop():
    global G15_INSTANCE
    for k in list(G15_INSTANCE.keys()):
        v = G15_INSTANCE[k]
        if 'node' in k:  # means namenode or datanode
            try:
                g15ec2.instances.filter(InstanceIds=[v["id"]]).terminate()
                G15_INSTANCE.pop(k, None)
            except Exception as e:
                print(e)
    return True


def launch_hadoop(n_datanodes):
    try:
        instance_config('load')
    except:
        pass
    destroy_hadoop()
    # namenode
    namenodetype = select_instance_type('namenode')
    g15_ins_namenode = g15ec2.create_instances(ImageId=IMAGEID, MinCount=1, MaxCount=1,
                                               SecurityGroupIds=[
                                                   G15_SG_ID.hadoop],
                                               InstanceType=namenodetype, KeyName=G15_SSH_KEY,
                                               BlockDeviceMappings=[{"DeviceName": "/dev/sda1",
                                                                     "Ebs": {"VolumeSize": 32}}],
                                               TagSpecifications=[{'ResourceType': 'instance',
                                                                   'Tags': [{'Key': 'Name', 'Value': 'Namenode'}, ]}])
    # datanodes
    datanodestype = select_instance_type('datanodes')
    g15_ins_datanodes = g15ec2.create_instances(ImageId=IMAGEID, MinCount=n_datanodes, MaxCount=n_datanodes,
                                                SecurityGroupIds=[
                                                    G15_SG_ID.hadoop],
                                                InstanceType=datanodestype, KeyName=G15_SSH_KEY,
                                                BlockDeviceMappings=[{"DeviceName": "/dev/sda1",
                                                                      "Ebs": {"VolumeSize": 32}}],
                                                TagSpecifications=[{'ResourceType': 'instance',
                                                                    'Tags': [{'Key': 'Name', 'Value': 'Datanode'}, ]}])
    store_instance_ip(g15_ins_namenode[0].id, 'namenode')
    count = 1
    for i in g15_ins_datanodes:
        store_instance_ip(i.id, f'datanode{count}')
        count += 1
    del count
    instance_config('store')

    # execute task


if __name__ == "__main__":
    from g15_config import *
    # initialize session and ec2
    g15session = get_aws_session()
    g15ec2 = g15session.resource('ec2')
    g15ec2client = g15session.client('ec2')
    initialize()
    if select_operation('web'):
        logging.info("Setting up WEB and database.")
        launch_web_db()
    number_datanodes = select_operation('hadoop')
    if number_datanodes:
        logging.info("Setting up hadoop cluster.")
        launch_hadoop(number_datanodes)
    print(G15_INSTANCE)
