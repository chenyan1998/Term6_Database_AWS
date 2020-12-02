while [ ! -f /var/lib/cloud/instance/boot-finished ]; do sleep 1; done
sudo apt update -y 
sudo apt remove python3 -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt remove python-3.5 -y
sudo apt remove python3.5-minimal -y
sudo apt remove python3-pip -y
sudo apt install python3.7 -y
wget https://bootstrap.pypa.io/get-pip.py
python3.7 get-pip.py
rm get-pip.py -f
pip3 install fastapi uvicorn sqlalchemy pymongo pymysql
sudo apt install nginx -y
sudo apt install unzip -y
unzip frontend.zip
sudo mv -t /var/www/html frontend/index.* frontend/*.css frontend/*.js
sudo mv frontend/nginxdefault /etc/nginx/sites-available/default
sudo nginx -s reload
cd frontend/
python3.7 -m uvicorn comm_db:app &

