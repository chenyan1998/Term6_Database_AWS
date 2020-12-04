#!/bin/bash
# start analytics
# to find a way to wait all datanodes live
sudo -u hadoop /opt/hadoop-3.3.0/sbin/start-dfs.sh && sudo -u hadoop /opt/hadoop-3.3.0/sbin/start-yarn.sh
sudo mongoexport --collection=kindle_metadata --out=/home/hadoop/projectData/kindle_metadata.json 'mongodb://34.202.163.148/kindle_metadata' -u test_user -p test_user
/opt/sqoop-1.4.7/bin/sqoop import --bindir /opt/sqoop-1.4.7/lib/ --connect jdbc:mysql://54.165.138.26/kindle_reviews?useSSL=false --table Reviews --username root --password '&V]xM);}^$ts&9U-hC[C'

sudo -u hadoop /opt/hadoop-3.3.0/bin/hdfs dfs -mkdir -p /input/
sudo -u hadoop /opt/hadoop-3.3.0/bin/hdfs dfs -mkdir -p /input/pcc/
sudo -u hadoop /opt/hadoop-3.3.0/bin/hdfs dfs -mkdir -p /output/
sudo -u hadoop /opt/hadoop-3.3.0/bin/hdfs dfs -put /home/hadoop/projectData/kindle_metadata.json /input/pcc/

#running code command skip take in namenode's private
python3.7 pearson_corr.py
python3.7 tfidf.py
sudo -u hadoop /opt/hadoop-3.3.0/bin/hdfs dfs -get /output/reviews_tfidf_dir
