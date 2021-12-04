import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import select
conn = psycopg2.connect(host="localhost", dbname="dvndb", user="dbuser", password="dbpwd")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()

cur.execute("LISTEN new_status;")
print("Waiting for notifications on channel 'new_status'")

while True:
    if select.select([conn], [], [], 10) == ([], [], []):
        print("More than 10 seconds passed...")
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print(f"Got NOTIFY: {notify.channel} - {notify.payload}")