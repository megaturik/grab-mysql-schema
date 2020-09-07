# grab-mysql-schema
Script dumps users, privileges and databases to sql format

simple output

[root@hola grab-mysql-schema]# ./schema.py 
```
Please enter root password for MySQL:
CREATE DATABASE IF NOT EXISTS `bitrix` CHARACTER SET = 'utf8' COLLATE = 'utf8_unicode_ci';
CREATE DATABASE IF NOT EXISTS `database1` CHARACTER SET = 'utf8' COLLATE = 'utf8_unicode_ci';
CREATE DATABASE IF NOT EXISTS `database2` CHARACTER SET = 'utf8' COLLATE = 'utf8_unicode_ci';
CREATE USER `zabbix`@'localhost'IDENTIFIED BY PASSWORD '*80D4898C5830124809D1A28F484657C500886A97';
CREATE USER `bitrix`@'%'IDENTIFIED BY PASSWORD '*60C42053CD12579BFD94BC513A965D1E594C72E9';
CREATE USER `user1`@'localhost'IDENTIFIED BY PASSWORD '*DD3DDFD20627CDEBE9B8CCEFF2B5981C7815FF29';
CREATE USER `user2`@'localhost'IDENTIFIED BY PASSWORD '*3AE68DC5285FA18C486A8D5758F095E73F1A0792';
GRANT SELECT, PROCESS, SUPER ON *.* TO 'zabbix'@'localhost';
GRANT USAGE ON *.* TO 'bitrix'@'%';
GRANT ALL PRIVILEGES ON `bitrix`.* TO 'bitrix'@'%';
GRANT USAGE ON *.* TO 'user1'@'localhost';
GRANT ALL PRIVILEGES ON `database1`.* TO 'user1'@'localhost';
GRANT USAGE ON *.* TO 'user2'@'localhost';
GRANT ALL PRIVILEGES ON `database2`.* TO 'user2'@'localhost';
```
