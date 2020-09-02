#!/usr/bin/python

import mysql.connector
import os.path
import re
import getpass

mysqluser= 'root'
mysqldatabase= 'mysql'
mysqlpassword= ''
host= '127.0.0.1'
unix_socket = '/var/lib/mysql/mysql.sock'

query_mariadb_users = ("SELECT user, host, password FROM user WHERE user!='root' and user!='' and user!='mariadb.sys' and user!='mysql'")
query_mariadb_dbs = ("SELECT SCHEMA_NAME,DEFAULT_CHARACTER_SET_NAME,DEFAULT_COLLATION_NAME FROM schemata "
                    "WHERE SCHEMA_NAME!='mysql' and SCHEMA_NAME!='test' and SCHEMA_NAME!='sys' "
                    "and SCHEMA_NAME!='performance_schema' and SCHEMA_NAME!='information_schema'")
query_percona_users = ("SELECT user, host, authentication_string FROM user WHERE user!='root' "
                      "and user!='mysql' and user!='mysql.session' and user!='mysql.sys' and user!=''")
query_percona_dbs = ("SELECT SCHEMA_NAME,DEFAULT_CHARACTER_SET_NAME,DEFAULT_COLLATION_NAME FROM schemata "
                    "WHERE SCHEMA_NAME!='mysql' and SCHEMA_NAME!='test' and SCHEMA_NAME!='sys' "
                    "and SCHEMA_NAME!='performance_schema' and SCHEMA_NAME!='information_schema'")

def get_mysqlpassword():
        mysqlpassword = getpass.getpass("Please enter root password for MySQL:")
        return mysqlpassword

def is_mariadb(mysqlpassword):
    cnx = mysql.connector.connect(user = mysqluser, database = mysqldatabase, password = mysqlpassword, unix_socket = unix_socket)
    cursor = cnx.cursor()
    query = ("select @@version_comment")
    cursor.execute(query)
    for version in cursor:
        match = re.search("^MariaDB Server$", version[0])
    if match:
        return True

def get_dbs(query,mysqlpassword):
    cnx = mysql.connector.connect(user = mysqluser, database = 'information_schema', password = mysqlpassword, unix_socket = unix_socket)
    cursor = cnx.cursor()
    cursor.execute(query)
    for (db, encoding, collation) in cursor:
        result = "CREATE DATABASE IF NOT EXISTS `{}` CHARACTER SET = '{}' COLLATE = '{}';".format(db, encoding, collation)
        print(result)

def get_users(query,mysqlpassword):
    cnx = mysql.connector.connect(user = mysqluser, database = mysqldatabase, password = mysqlpassword, unix_socket = unix_socket)
    cursor = cnx.cursor()
    cursor.execute(query)
    for (user, hostname, password) in cursor:
        result = "CREATE USER `{}`@'{}'IDENTIFIED BY PASSWORD '{}';".format(user, hostname, password)
        print(result)
    cursor.execute(query)
    for (user, hostname, password) in cursor:
        user = "`{}`@'{}'".format(user, hostname)
        get_grants(user,mysqlpassword)
    cursor.close()
    cnx.close()

def get_grants(user,mysqlpassword):
    cnx = mysql.connector.connect(user = mysqluser, database = mysqldatabase, password = mysqlpassword, unix_socket = unix_socket )
    cursor = cnx.cursor()
    query = ("SHOW GRANTS FOR {};".format(user))
    cursor.execute(query)
    for user in cursor:
        result ="{};".format(user[0])
        print(result)

mysqlpassword = get_mysqlpassword()    
is_mariadb = is_mariadb(mysqlpassword)

if is_mariadb == True:
    get_dbs(query_mariadb_dbs,mysqlpassword)
    get_users(query_mariadb_users,mysqlpassword)
else:
    get_dbs(query_percona_dbs,mysqlpassword)
    get_users(query_percona_users,mysqlpassword)
