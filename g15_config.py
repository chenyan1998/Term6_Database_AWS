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


CRED = """aws_access_key_id=ASIAQ6R4KCM7RHA7B67V
aws_secret_access_key=3H1EHFfMs+EK4CdGsc8lZW3NZfn9nmfsiFJurMFb
aws_session_token=FwoGZXIvYXdzECgaDD7rgtJw9UCineIe7SLOAVomEfwWAByqR76QOPSQcMrpSqqfsLerrCubWFkKCOfrK4qGq7rXRYvu8/FFtuWRZQsP0LPFN3FOzE/T43KzCbeEedZvEoZ6a8OygU7KOh0H36v+itgzMj+Pq1EIW2q8WQnaqvEazlXq79jSbES2WYPjEor4lN9fIZh59zdBUrnSCKG5duWkVwKizGZuaVq8DIjyFUa9j34CS9XWLD03RE335a3Lr3JgTp0LZb3NMrXbpPGsKbcV5nV0YAYHtTR/kP2iV7f6BUskNLCyDiOMKPvjnP4FMi1z9GTmsW4wkrf5v07wd9fGCSr52LS6If4UYA+GIzzlfENaqIJwh/S5dOCXAFY="""
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
