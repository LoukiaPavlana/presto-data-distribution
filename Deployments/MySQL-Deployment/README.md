### MySQL Deployment

#### References

** Installation Guide[https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/data-directory-initialization.html]

#### Overview
MySQL is a very popular Realational DBMS used for a variety of projects, of various scales. It is released under an open-source licence, it uses a standard form of the well-known SQL data language and has great compatibility on many operating systems. It will be used as part of the 3 databases comprising our trino experiments.

#### Deployment
##### Download and Install
    sudo apt update
    sudo apt install mysql-server
    sudo mysql_secure_installation
    sudo systemctl start mysql
    sudo systemctl enable mysql
2. Create new user:
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
3. Grant Permissions:
GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
FLUSH PRIVILEGES;
4. Create Database:
CREATE DATABASE mydb;
5. Access Database:
USE mydb;
6. Create table:
CREATE TABLE employees (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), position VARCHAR(255));

## Start MySQL

1. 
    
    ![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/76d97b0a-80da-4d19-89b9-63074569edb2/c7c719d4-a152-4f41-bca1-3586e28983cd/image.png)
    
2. password: rRm4R3xGCH (required once)
3. show databases:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/76d97b0a-80da-4d19-89b9-63074569edb2/1758c0cc-7522-459c-9bf6-0704e51c91b5/image.png)

### Change Authenticaiton Plugin for root

```jsx
sudo mysql
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'secret';
FLUSH PRIVILEGES;
```

### Change bind-address

```jsx
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
```

from: bind-address            = 127.0.0.1

to:      bind-address            = 0.0.0.0
