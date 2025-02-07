# MySQL Deployment

## References

** Installation Guide[https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/data-directory-initialization.html]

## Overview
MySQL is a very popular Realational DBMS used for a variety of projects, of various scales. It is released under an open-source licence, it uses a standard form of the well-known SQL data language and has great compatibility on many operating systems. It will be used as part of the 3 databases comprising our trino experiments.

## Deployment
### Download and Install
    sudo apt update
    sudo apt install mysql-server
    sudo mysql_secure_installation
    sudo systemctl start mysql
    sudo systemctl enable mysql
### Connecting   

When MySQL was created these were the default parameters:

* user → root
* password→ blank

Connect to MySQL:
```
    sudo mysql -u root -p
```    
Create new user:
```
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password'; 
```
Grant Permissions:
```
GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
FLUSH PRIVILEGES;
```
Create Database:
```
CREATE DATABASE mydb;
```
Access Database:
```
USE mydb;
```
Create table:
```
CREATE TABLE employees (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), position VARCHAR(255));
```

