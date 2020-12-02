class sg_ids:
    """a class to store security group ids"""

    def __init__(self):
        self.web = ''
        self.mysql = ''
        self.mongo = ''
        self.hadoop = ''


class ips:
    def __init__(self, ins_id='',pri='', pub=''):
        self.id = ins_id
        self.private = pri
        self.public = pub


class instances:
    def __init__(self, num_datanodes):
        self.web = ips()
        self.mysql = ips()
        self.mongo = ips()
        self.namenode = ips()
        self.datanodes = []
        for _ in range(num_datanodes):
            self.datanodes.append(ips())


CRED = """aws_access_key_id=ASIAQ6R4KCM765UPHNI7
aws_secret_access_key=SnAMm6Hkeoz1MJw1abPQYBesXkj6QzeF8fWrQTqe
aws_session_token=FwoGZXIvYXdzEC8aDCSA03ugG+7g7LtVBSLOAXnEra3UTYREDl9jbP4sbhpEYkJ5GqF9B27qaRah81ak4D80uzTJOaMc88CvmE+jjM/Xq9HCKiyTLZz/KuEHto6vqnYyC6TDLqAMO6BOOMSLHYAISM1jhd0ncPto/nchANFq57btXbbbGtfDwNHvfRlGLDkhAX8jkzBfgP2Y1eYBNBZ/oYSRgeXDQ4gdY6QAX1LcEsjQNDDm0c3bTOxUHiaazsFRG1DG7TY8IxFioNrbmy74jr2IAi9cs1ChWRpVgb5m7dIydwjOhjivjxWhKMK6nv4FMi0kdV7rRZdOMe3am7EW4BNprZr8mBNJrzCmhDDEpyMIWM+0QL+GxZ4kk94lbTA="""
IMAGEID = "ami-0f82752aa17ff8f5d"
G15_SSH_KEY = "g15key"
G15_SSH_KEY_PEM = ""
G15_SG_WEB = "g15_web_sg"  # WEB security group
G15_SG_WEB_DESC = "for web"
G15_SG_MONGO = "g15_mongodb_sg"  # mongodb security group
G15_SG_MONGO_DESC = "for mongodb"
G15_SG_MYSQL = "g15_mysql_sg"  # mysql security group
G15_SG_MYSQL_DESC = "for mysql"
G15_SG_HADOOP = "g15_hadoop_sg"  # hadoop security group
G15_SG_HADOOP_DESC = "for hadoop"
G15_SG_ID = sg_ids()
G15_VPC_ID = ''
G15_INSTANCE = {}

G15_INSTANCE_TYPE = {1: "t2.micro", 2: 't2.small',
                     3: 't2.medium', 4: 't2.large', 5: "t2.xlarge"}
G15_SELECT_ASK = ''
