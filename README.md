# 50.043 DataBase And Big Data Systems group project
2020 Term6 *Group 15*

```
Chen Yan         1003620
Zhang Shaozuo    1003
Hua Guoqiang     1003783
Chi Ziheng       1003
```

The project is aiming to do a web application for Kindle book reviews and a system to analyze the statistics. 

This repository contains the necessary code to run this web application and analytics system plus an automation script which sets up the whole system automatically.

## Usage

### Set up environment
This automation script is written by Python and requires Python 3.7 or higher to run.

You need to install AWS Command Line Interface to run this programme. More information about AWS CLI can be found here: [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/). Please follow the instructions to install AWS CLI on your system.

You need also run the following code to install some necessary modules.

```
python3 -m pip install boto3 --user
python3 -m pip install paramiko --user
```


### Set up credentials
To run the automation process, you need to first put your AWS credentials in `g15_config.py`, `CRED` variable. Please make sure the credentials are in tripple quotes.

The credentials will be something like:
```
aws_access_key_id=ASIAQ6R4KCM7547T6YGH
aws_secret_access_key=ak0Xmj1zmYB5+9a8rca8LPbS5Owmp6SmIEMpwSFp
aws_session_token=FwoGZXIvYXdzEHQaDOHqdRmYfE1fKPbuqiLOAY6ng/nu7PxxEC6moRopnfY2NMBuy2Ru2ZapKs5Ur44zAk9MFGmZ9hiSBJSLirR66cTMxhyKh9px22budnmCNw/LQzV9n45lWnNq9RcC1koECTy/886zuvATZrW95hpFaXj47qw09bDogfYzLOlAxuaLuRjs+RVSsFu92KczItXpAPzulRhuo5Ux/rF+WDhCVVvySJdG9FZ2C41YWUL6jloXa9jtcqF/nQfNh1zP5pkDC8QBYttpn9GLNrgchHsnF641vM77akCGfex6ved7KODPrf4FMi1kGqKxgoRaz04DTK+AySNF2uytfEouBJ4vnM76qxUmNeyJHHjnZCFoDuNKizA=
```

You can also customize your preferred `IMAGEID` in `g15_config.py`.

### Automate it !
After finishing setting the credentials, you can directly run `g15automation.py` to automatically set up the whole system.

There are some simple prompts in the process of running and you may need to answer *yes/no* or *input* some numbers for some prompts 

<br>

<details>
<summary>Some prompts</summary>

#### Setting up WEB and database
A prompt will ask you:
```
Setup WEB and Database?
(1) Yes (2) No
```

- Yes, the programme will set up WEB frontend instance, MySQL instance and MongoDB instance.
- No, skip this setup.

#### Setting up Hadoop cluster
A prompt will ask you:
```
Setup Hadoop cluster?
(1) Yes (2) No
```

- Yes, the programme will ask you how many datanodes you need and you shall input a number. And it will set up one namenode instance plus your desired number of datanode instances.
```
Please input how many datanodes you want to setup.
```
- No, skip this setup.

#### Clean up
A prompt will ask you:
```
Tear down everything?
(1) Yes (2) No
```

- Yes, the programme will terminate the instances it created so far and delete security groups it has created.
- No, skip this process.
</details>

<br>

### Note
1. It is not necessary that you run the clean process after setting up. You can always re-running this script with skipping the set up process (by choosing *no*) to reach the clean up process.
2. After setting up, you can easily scale up and down the Hadoop cluster by re-running this script with skipping **WEB and database** process and inputting your desired number of datanodes. The script will automatically **delete** the old cluster and build a new one. **NOTE: Please BACKUP your cluster BEFORE you scale up and down, the script WILL NOT keep your data**

