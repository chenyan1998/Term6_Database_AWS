while [ ! -f /var/lib/cloud/instance/boot-finished ]; do sleep 1; done
sudo apt-get update
sudo apt install unzip

echo "Installing MongoDB"
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod

echo "Openning MongoDB port for remote connection" 
sudo sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mongod.conf
sudo systemctl restart mongod
sleep 5 #wait for restart to finish

echo "Downloading kindle metadata"
#wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/meta_kindle_store.zip -O meta_kindle_store.zip
#wget -c https://github.com/chiziheng/ziheng-s-first-repo/blob/main/kindle_metadata_final.zip?raw=true --output-document=kindle_metadata_final.zip
wget --output-document=kindle_metadata_final.json https://raw.githubusercontent.com/chenyan1998/50043.DataBase_And_BigData/main/kindle_metadata_final.json?token=AJT3LRAUS3WKGFQTU56TKES7Y6CGS

#echo "Unzipping metadata file"
#unzip kindle_metadata_final.zip

echo "Downloading mongodb commands and execute"
wget --output-document=mongo_commands.js https://raw.githubusercontent.com/chenyan1998/50043.DataBase_And_BigData/main/mongo_commands.js?token=AJT3LRB3VQ3K3BTUIWZ2FF27Y6B3K
mongo < mongo_commands.js

echo "Importing data in to mongodb"
mongoimport --db kindle_metadata --collection kindle_metadata --file kindle_metadata_final.json --legacy
sudo sed -i 's/#security:/security:\n  authorization: enabled/g' /etc/mongod.conf # enable authantication for mongodb
sudo systemctl restart mongod
#mongo --eval kindle_metadata 'db.kindle_metadata.remove({title: { $exists: false }})'
rm -rf mongo_commands.js kindle_metadata_final.json Mongodb_setup_script.sh

echo "MongoDB setup finished"

#sed -i -e 's/\r$//' Mongodb_setup_script.sh
