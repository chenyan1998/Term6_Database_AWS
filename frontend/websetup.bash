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
