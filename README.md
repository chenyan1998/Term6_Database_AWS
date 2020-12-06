<h1>50.043 DataBase And Big Data Systems group </h1>project
2020 Term6 *Group 15*

```
Chen Yan         1003620
Zhang Shaozuo    1003756
Hua Guoqiang     1003783
Chi Ziheng       1003030
```

# 1. Introduction
The project is aiming to do a web application for Kindle book reviews and a system to analyze the statistics. An automation script to set up the whole system is also requrired.

This repository contains the necessary code to run this web application and analytics system plus an automation script which sets up the whole system automatically.

## Instances
We need several AWS instances to run the system.
- Front end
  - web server
  - MySQL server
  - MongoDB server

- Hadoop cluster
  - Namenode
  - Datanode1
  - Datanode2
  - Datanode3
  - ...


## 1.1. File structure and role

There are some template files and some values such as IP and hostname need to be changed to set up the whole system. **Note that this will be AUTOMATICALLY DONE by automation script which is `g15automation.py`**, you don't need to worry about this.

<details><summary>Click to expand</summary>

- analytics_template
  - `pearson_correlation.py`
    
    A python script to calculate Pearson correlation between review length and book price.
  - `tfidf.py`
    
    A python script to calculate TF-IDF values of words in review texts.
- frontend_template
  - `comm_db.py`
    
    A python script to serve as a middleware between web application and databases.
  - `config.py`

    A **template** configuration file to store database connection details such as IP, port and password.
  - `index.html`
    
    Front end HTML file which determines structure of the web page.
  - `main.css`
    
    Front end cascading style sheets which decorates the web page.
  - `main.js`
    
    A **template** JavaScript file which determines the interaction logic of front end.
  - `web.bash`
    
    A shell script to set up web server.
  - `nginxdefault`

    An Nginx configuration to configure web server and a reverse proxy for the middleware.
  - `axios.min.js`
    
    Necessary JavaScript library.
  - `style.css`
  - `vue.js`

    Necessary JavaScript library.
  - `vxe-table.js`

    Necessary JavaScript library.
  - `xe-utils.js`

    Necessary JavaScript library.

- hadoop_template
  - `namenode.bash`

    A **template** shell script to set up namenode.
  - `datanode.bash`

    A **template** shell script to set up datanode.
  - `analytics.bash`

    A **template** shell script to start HDFS system, inject the data and run analytics python code.
- mongo
  - `mongo.bash`

    A shell script to set up MongoDB server and import data to MongoDB.
  - `mongo_commands.js`

    A MongoDB script to create database structure and users.
  - `kindle_metadata_final.zip`

    Kindle books metadata.
- mysql
  - `mysql.bash`

    A shell script to set up MySQL server.
  - `sql_commands.sql`

    A MySQL script to create database structure, create users and import data to MySQL.
- `g15_config.py`
    
    A congiuration file to store some parameters such as IMAGEID.
- `g15automation.py`

    An automation script to set up the whole system.
- `README.md`
- `.gitignore`

</details><br>


## Web application features

### Search
Users can search books by title in the top bar of the home page. The searching result of the related book information(title,image,category,description and price) will show in a list.

### Pagination
If there are more than 50 results, the page will only show the first 50 results. You can click next page button located on the top to view the next 50 results.

### Add a new book
User can add a new book at the homepage by manual input book attributes(eg. ASIN number, title, imUrl and description) to the database in the top bar of the home page.

### Add a new review
After users arrive at the search result page, they can click a book title and add a new review manually at the pop-up window to the database.

### Sort book by genre
After you perform a search and get some results, you can click a genre in category column and the page will show the results in this genre.

### Reviews sort by time
Users can sort reviews by time at the pop-up view details window. They can click the ‘Sort by time’ button to sort reviews. 

<details>
<summary>Some screenshots</summary>

</details>
<br>

## 1.2. Usage

### 1.2.1. Set up environment
This automation script is written by Python and requires Python 3.7 or higher to run.

You need to install AWS Command Line Interface to run this programme. More information about AWS CLI can be found here: [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/). Please follow the instructions to install AWS CLI on your system.

You need also run the following code to install some necessary modules.

```
python3 -m pip install boto3 --user
python3 -m pip install paramiko --user
```


### 1.2.2. Set up credentials
To run the automation process, you need to first put your AWS credentials in `g15_config.py`, `CRED` variable. Please make sure the credentials are in tripple quotes.

The credentials will be something like:
```
aws_access_key_id=ASIAQ6R4KCM7547T6YGH
aws_secret_access_key=ak0Xmj1zmYB5+9a8rca8LPbS5Owmp6SmIEMpwSFp
aws_session_token=FwoGZXIvYXdzEHQaDOHqdRmYfE1fKPbuqiLOAY6ng/nu7PxxEC6moRopnfY2NMBuy2Ru2ZapKs5Ur44zAk9MFGmZ9hiSBJSLirR66cTMxhyKh9px22budnmCNw/LQzV9n45lWnNq9RcC1koECTy/886zuvATZrW95hpFaXj47qw09bDogfYzLOlAxuaLuRjs+RVSsFu92KczItXpAPzulRhuo5Ux/rF+WDhCVVvySJdG9FZ2C41YWUL6jloXa9jtcqF/nQfNh1zP5pkDC8QBYttpn9GLNrgchHsnF641vM77akCGfex6ved7KODPrf4FMi1kGqKxgoRaz04DTK+AySNF2uytfEouBJ4vnM76qxUmNeyJHHjnZCFoDuNKizA=
```

You can also customize your preferred `IMAGEID` in `g15_config.py`.

### 1.2.3. Automate it !
After finishing setting the credentials, you can directly run `g15automation.py` to automatically set up the whole system.

There are some simple prompts in the process of running and you may need to answer *yes/no* or *input* some numbers for some prompts 

<br>

<details>
<summary>Some prompts</summary>

#### 1.2.3.1. Setting up WEB and database
A prompt will ask you:
```
Setup WEB and Database?
(1) Yes (2) No
```

- Yes, the programme will set up WEB frontend instance, MySQL instance and MongoDB instance.
- No, skip this setup.

#### 1.2.3.2. Setting up Hadoop cluster
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

#### 1.2.3.3. Clean up
A prompt will ask you:
```
Tear down everything?
(1) Yes (2) No
```

- Yes, the programme will terminate the instances it created so far and delete security groups it has created.
- No, skip this process.
</details>

<br>

### 1.2.4. Note
1. It is not necessary that you run the clean process after setting up. You can always re-running this script with skipping the set up process (by choosing *no*) to reach the clean up process.
2. After setting up, you can easily scale up and down the Hadoop cluster by re-running this script with skipping **WEB and database** process and inputting your desired number of datanodes. The script will automatically **delete** the old cluster and build a new one. **NOTE: Please BACKUP your cluster BEFORE you scale up and down, the script WILL NOT keep your data**

