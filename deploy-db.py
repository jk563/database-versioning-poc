import mysql.connector
from os import listdir
import sys

upgrade = False
downgrade = False

target_version = int(sys.argv[1])

connection = mysql.connector.connect(user='root', password='password')
cursor = connection.cursor()

try:
    query = ("USE db;")
    cursor.execute(query)
    query = ("SELECT version FROM db_versioning;")
    cursor.execute(query)
    current_version = int(cursor.fetchone()[0])
except mysql.connector.ProgrammingError:
    current_version = 0

print(f"Target Version: {target_version}")
print(f"Current Version: {current_version}")
if target_version == current_version:
    print("Nothing to do")
    sys.exit()
elif target_version > current_version:
    upgrade = True
    scripts_directory = 'upgrade-scripts'
    print(f"Upgrading from {current_version} to {target_version}")
elif target_version < current_version:
    downgrade = True
    scripts_directory = 'downgrade-scripts'
    print(f"Downgrading from {current_version} to {target_version}")

all_scripts = sorted(listdir(scripts_directory))
if upgrade:
    scripts_to_run = all_scripts[current_version:target_version]
if downgrade:
    scripts_to_run = all_scripts[target_version:current_version]
    scripts_to_run.reverse()

print("Scripts to run:")
print(scripts_to_run)

for script in scripts_to_run:
    script_number = int(script[:3])
    print(f"Running: {script}")
    script_file = open(f"{scripts_directory}/{script}", 'r')
    sql = script_file.read()
    script_file.close()
    commands = sql.split(';')
    for command in commands:
        if len(command) > 1:
            cursor.execute(command)
    if upgrade or (downgrade and script_number != 1):
        new_db_version_number = script_number if upgrade else script_number - 1
        query = (
            f"UPDATE db_versioning SET version = {new_db_version_number};"
        )
        cursor.execute(query)
        connection.commit()

cursor.close()
connection.close()

print("Finished")
