# Database CI PoC
This proof of concept demonstrates a method of being able to automatically upgrade and downgrade databases in order to be able to automate changes to them and integrate them with delivery pipelines.

## Overview
Different environments will have databases that are a different version from one another. By treating the database as a versioned item and having migration scripts from each version to the next, we can take a database of any version and sequentially run the appropriate migration scripts to take it to any other version.

This database deployment script expects `upgrade-scripts` and `downgrade-scripts` directories which hold the relevant scripts in order. The database has a table with a row giving the database's current version. This is used along with an argument passed to the script to determine which scripts will be run. Each script in `upgrade-scripts` has an equivalent script with the same name in `downgrade-scripts` which acts as the rollback for that migration. 

## Prerequisites
Docker - `brew install docker`  
MySQL Client - `brew install mysql`  
Python3 - `brew install python3`  
Python MySQL Connector - `pip3 install mysql-connector-python --user`

## Running the PoC
To check the internal database version (exists when the db is at v1+), you can run  
`mysql -h 127.0.0.1 -u root -ppassword < queries/db_version.sql`

1. Start up a MySQL server  
`docker run --name mysqlserver -p 3306:3306 -e MYSQL_ROOT_HOST=% -e MYSQL_ROOT_PASSWORD=password --detach mysql/mysql-server`
2. Run the database deployment script to version 2  
`python3 deploy-db.py 2`
3. Insert test data  
`mysql -h 127.0.0.1 -u root -ppassword < test-data/test-data.sql`
4. Check the person table contents  
`mysql -h 127.0.0.1 -u root -ppassword < queries/person_table.sql`
5. Upgrade the database to version 3  
`python3 deploy-db.py 3`
6. Check the person table contents  
`mysql -h 127.0.0.1 -u root -ppassword < queries/person_table.sql`
7. Downgrade the database to version 2  
`python3 deploy-db.py 2`
8. Check the person table contents  
`mysql -h 127.0.0.1 -u root -ppassword < queries/person_table.sql`
9. Upgrade the database to version 3  
`python3 deploy-db.py 3`
10. Check the person table contents  
`mysql -h 127.0.0.1 -u root -ppassword < queries/person_table.sql`
11. Stop the container  
`docker stop mysqlserver`
12. Remove the container  
`docker rm mysqlserver`

