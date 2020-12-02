class sg_ids():
    def __init__(self):
        self.web = ''
        self.mysql = ''
        self.mongo = ''
        self.hadoop = ''

CRED = """aws_access_key_id=ASIAQ6R4KCM7XHJQRE7D
aws_secret_access_key=mwJOkmsmQGhCZ/n/DKw1Tu6TJ1MkQrL8vW+s05wc
aws_session_token=FwoGZXIvYXdzECQaDCCy432U0oi7XCY79iLOAbJu4gPkxOkiND/zXkpXE9LKXAHyUOjbdgCZNXQ2KoJd9iNYBm1ZSDxXFThqi7voavN5ygXHUt6nSwtgayCP1+pq+vQwRMDYdjxWOHnxtYrHTXizJ6ZPa5CWCMSHVfFnYKApLtX368zRmP2+G8ZL7Nfk6Mf+Av2RDUR1tG8I/soULUSzBZDbzH4shwM4nkwlC6aajmIvAFLwwxaymWjWLB1Ig1CSb3XfZChUdMNSg7dozFmm+5MaZerVstmVf0HhcqSn0GJnEuzJBOSWl373KMDym/4FMi2/dzG4KUMr3FyT2mbBLu3NwlgRNdepQ8b9iSrVne2zCLIsCdDVv6TWaYRutk4="""
IMAGEID = "ami-0f82752aa17ff8f5d"
G15_SSH_KEY = "g15key"
G15_SG_WEB = "g15_web_sg" # WEB security group
G15_SG_WEB_DESC = "for web"
G15_SG_MONGO = "g15_mongodb_sg" # mongodb security group
G15_SG_MONGO_DESC = "for mongodb"
G15_SG_MYSQL = "g15_mysql_sg" # mysql security group
G15_SG_MYSQL_DESC = "for mysql"
G15_SG_HADOOP = "g15_hadoop_sg" # hadoop security group
G15_SG_HADOOP_DESC = "for hadoop"
G15_SG_ID = sg_ids()
G15_VPC_ID = ''
