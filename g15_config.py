class sg_ids:
    """a class to store security group ids"""

    def __init__(self):
        self.web = ''
        self.mysql = ''
        self.mongo = ''
        self.hadoop = ''


CRED = """aws_access_key_id=ASIAQ6R4KCM7V4TI54NZ
aws_secret_access_key=RzDhHMEn9HqeTAMT2ozD8CCrHoYIsF/y/Q8tEqlK
aws_session_token=FwoGZXIvYXdzEGEaDMVygULSGajNYNPq5iLOAd+/6twO1/X91uyhYBL7Fy7ZA7ZUGiIS/Y+1diLd/E62lcE0akyLxwZL0UoI+RKrrfyDxkUU7EhL0uuPcC9aMQ/ITEI0SYYYj0qEKKKhUxGIVFMTBf1YYgdSues1Nd8UHfaYbQec3UYEr1x9W3sh2FvrVIASfCm+2YnFoBHS0PJoOArh+JVL6/xSIs+32dmF4eVdfqvDqGEAuw5EJNN03TNg3nidv0GIfkr3qAOmXDrJASMR9ExERoot0Bg1JryLzSZWSjnj4i2aiUNYlJaLKJCyqf4FMi2dJuBfOA9ByZ31jgxbd8uYxUAFWrlMEKxszNmpxNlLo8iNDBHHrLsbIaBKiPA="""
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
