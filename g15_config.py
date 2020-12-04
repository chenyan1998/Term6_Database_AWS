class sg_ids:
    """a class to store security group ids"""

    def __init__(self):
        self.web = ''
        self.mysql = ''
        self.mongo = ''
        self.hadoop = ''


CRED = """aws_access_key_id=ASIAQ6R4KCM7RJJDAABV
aws_secret_access_key=CdFxUlN0Wh+V5DS+Vigct+cm4ElDl0L8ohfZmame
aws_session_token=FwoGZXIvYXdzEFsaDPct/LdLkOFjp/ulVCLOAdmajZicCUv47YrNV0fYRz1nZet4GNAg6yHZ1+TmDUStYPuXmnL5njz3c56J8scEhw9WBy+xFfekwBRA8KnL/rp8kdNNZqDntLVnsEdxbDd9IkUuYTfLUyPYsmsnCoRUcICGwyAmMvKjDqSYxLiw90+zUBXYcVpPpSTqkDZJHtycQueBG627ZIXMA1lAnNBuy5Cxpjj1YdlSo96NjllF3ot/DNVW3CTGwv2MEJdKgsNxmypOEwmZgLa8I8Y0F7RBBqVlMpBvuMwhnI6ni5m9KNmCqP4FMi2lDRWleOYYrNLcBndA4VpmSGALmblrE5QIyRzHEIvqA/j4/2hXSDoIDw+eM+I="""
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
