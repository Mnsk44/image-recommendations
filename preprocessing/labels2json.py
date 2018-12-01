import psycopg2
import sys
import pickle
import json

# Database details
dbname = 
host = 
port = 
user = 
pwd = '

try:
    conn = psycopg2.connect(dbname=dbname, host=host, port=port, user=user, password=pwd)
    print("Connecting to Database")
    cur = conn.cursor()
    
    cur.execute("SELECT DISTINCT (labels) labels FROM omaluokittelu ORDER BY labels ASC;")

    #data = cur.fetchone()
    #data = cur.fetchmany(10)
    data = cur.fetchall()
    
    labels = []
    for i, label in enumerate(data, 1):
        labels.append({"data":i, "value":label[0]})

    with open("labels.json", mode="w") as json_file:
        json.dump(labels, json_file, indent=3)

    conn.close()
    print("DB connection closed.")

except Exception as e:
    print("Error: {}".format(str(e)))
    sys.exit(1)

