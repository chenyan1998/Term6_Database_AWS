class sg_ids:
    """a class to store security group ids"""

    def __init__(self):
        self.web = ''
        self.mysql = ''
        self.mongo = ''
        self.hadoop = ''


CRED = """aws_access_key_id=ASIAQ6R4KCM7YLFRMWMB
aws_secret_access_key=9OPTgDvfqdavXVBAxtwu1TdaxvRGj+SqgtxR9kBy
aws_session_token=FwoGZXIvYXdzEGsaDDbxJj9AYbiRuJpiwSLOAVqFaveCytaCp3PdOO1pa3uTv1a0aFTnooUPiiAV+Jf1FH8bdlqcWJ9Q+5BfuyBDokkWfdsPXH+vHMzPAvZy+WW0NVFpakbsZWtnxNZPZA/B3irPsmUUAYjtSxRRmLYYtIerRjwMFEhSJuSsc7As8Pkjh//RBLE05+JjCSatEMAmXKRlKpA7yYlpZORba7DikCmqeVWuV0pO4kJSa9+HP4nUuTmKrp8fjUuLBVWID0DHCkKxgCqqlaH3+awCP1mMq9lr6IH+UbuxDCFBzBt6KO3Hq/4FMi3xghm3D0OnpQgH7Oejp4lkt6nUFvpjqb1Dtb3qDajf/ZjEPgrvzk/jiEm4VRQ="""
IMAGEID = "ami-0f82752aa17ff8f5d"
G15_SSH_KEY = "g15key"
G15_SSH_PUBKEY = "g15pubkey"
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
