from os import write
from pickle import TRUE
import time
import paramiko
import pickle
from io import StringIO

k = paramiko.RSAKey.from_private_key(
    StringIO(pickle.load(open("g15key", 'rb'))))
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("connecting")
c.connect(hostname="54.162.188.143", username="ubuntu", pkey=k)
print("connected")


c.exec_command("sudo dpkg --configure -a",get_pty=True)
(stdin, stdout, stderr) = c.exec_command("sudo apt install mysql-server -y")
while not stdout.channel.exit_status_ready():
    stdin.write('\n')
    stdin.flush()
    print(1)
    time.sleep(0.5)


    

print(stdout.read())


c.close()
del stdin, stdout, stderr