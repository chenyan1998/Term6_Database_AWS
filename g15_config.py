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


CRED = """aws_access_key_id=ASIAQ6R4KCM73KAN6GEJ
aws_secret_access_key=6GXlKwbhD5rvMnsKi+2A9b2r91LbKIgcsF2yN2KH
aws_session_token=FwoGZXIvYXdzECwaDE6HFJ7pjrmWpgvHsiLOAWsZmQ1Cp7b2+RXPtS8WWcXRhDxqtgAr8cIqkPWo1cib4wJnvg219fJo5s9HUyezVZH9P268S+mJcUkPl+fpdrlSO2EFWZHklfJHSX+RBxGGaymzLwVgY0HuVLsXeunrTOiKMSRe5fNMzP8iyL6JzQAH/oFrZMUJrJOVZ36fceV0ts7lDeYeIssA8BdwQ219+6R4is+6HFwEgO/UnUmWDDIutrKnakol9rFjyA2vE2mw+iqm/rENJRiamhXd7E9zv9AExNpgWMmjMlvENMv6KIfgnf4FMi1RisXNjHnIDMgiAwQZJ62bkgcdiibMG6+BBEIU7iOz+uBFeBDxJ5sGSeVa2VI="""
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
