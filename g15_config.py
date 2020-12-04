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


CRED = """aws_access_key_id=ASIAQ6R4KCM7YQDUCXVX
aws_secret_access_key=Bwt52jGnbtQEu4rVD7lXNhxJsdyHz+nmD1PtUmRC
aws_session_token=FwoGZXIvYXdzEFcaDL6iBNJFsejub6bbXCLOAYLJmsjWow4moct9Ybk9aE5LNpzyjjrFLVckfTq/h1eRyl3wNZ+9wWLm9+5wPtLQuUNzZOSUpWXQwyoB5lHv/mgpwGsxIxYF+i8F7xouR9FwoPGtL6lD1KWbHeQ5vjn0cuEikLSKLXUvWrs1QNIaM2bSMFoc6qRh6RzIoQ7W+27Y4Hx/C0FN/e/dXO2W0HmLtRyUc8cAkqPZStv1ut3TBqVnSU49AVVCURIH8q1+dSbBs9XTu8KEl2IWPDoQZQQfy1nshG7OwgLiQPUsMkmWKK6Hp/4FMi2iL7Gt12iVZnqVRi8QQf994mO7tNjmISdlIb9DOxTJmkI0ANJE1EYjbP2YxPg="""
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
