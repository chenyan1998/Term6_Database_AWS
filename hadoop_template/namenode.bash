#!/bin/bash
while [ ! -f /var/lib/cloud/instance/boot-finished ]; do sleep 1; done
while [ ! -f /var/lib/cloud/instances/i-*/boot-finished ]; do sleep 1; done
sudo apt update -y
sudo apt install ssh -y
echo "ip com.g15.namenode" | sudo tee -a  /etc/hosts
echo "ip com.g15.datanode1 " | sudo tee -a  /etc/hosts
sudo hostnamectl set-hostname com.g15.namenode
sudo adduser --disabled-password  --gecos '' hadoop
sudo sh -c 'echo "hadoop ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/90-hadoop'
sudo sysctl vm.swappiness=10
sudo su - hadoop


http://mirror.cogentco.com/pub/apache/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz