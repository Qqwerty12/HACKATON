import mysql.connector
from mysql.connector.constants import ClientFlag
import pandas as pd
from geopy import distance
import requests
import json
config = {
    'user': 'root',
    'password': 'Zero2009',
    'host': '34.150.58.112',
    'client_flags': [ClientFlag.SSL],
    'database' : 'testdb',
    'ssl_ca': 'C:/Users/unifo/Desktop/hackaton/server-ca.pem',
    'ssl_cert': 'C:/Users/unifo/Desktop/hackaton/client-cert.pem',
    'ssl_key': 'C:/Users/unifo/Desktop/hackaton/client-key.pem'
}


cnxn = mysql.connector.connect(**config)

cursor = cnxn.cursor()  # initialize connection cursor
#cursor.execute('CREATE DATABASE testdb')  # create a new 'testdb' database
#cursor.execute('''CREATE TABLE customers1 (id_order INT, id_pos INT, ord_status
#VARCHAR(255), full_name VARCHAR(225), email_address VARCHAR(225),
 #phone VARCHAR(225), address_in VARCHAR(225), address_out VARCHAR(225),price INT, weight INT(11))''')
  #sql = "INSERT INTO customers1 (id_order, id_pos, ord_status, full_name, email_address, 
  #phone, address_in, address_out, price, weight) VALUES (2, 1, 'delivering', 'Loldaskek', '1example.gmail.com', '8123838222', 'Nur-Sultan', 'Almata', 26000, 9)"
#cursor.execute(sql)
cnxn.commit()
cursor.execute("SELECT * FROM customers1")
myresult = cursor.fetchall()
for x in myresult:
  print(x)
#cursor.execute("DROP TABLE customers1")
#cnxn.commit()


def calculate(wei, prc_prod, ln):
    prc_road = 250
    cost_prod = wei*prc_prod
    cost_road = ln * prc_road
    ttl = cost_prod + cost_road
    return ttl
cursor.execute("SELECT id_order, ord_status, SUM(price*weight) FROM customers1 GROUP BY id_order, ord_status")
myresult = cursor.fetchall()
for x in myresult:
  print(x)
df = pd.read_csv("C:/Users/unifo/Desktop/hackaton/concap.csv")

# rename so that the column names are shorter and comply with PEP-8
df.rename(columns={"CountryName": "Country", "CapitalName": "capital", "CapitalLatitude": "lat", "CapitalLongitude": "lon", "CountryCode": "code", "ContinentName": "continent"}, inplace=True)
ropa = df[df["capital"].isin(["Rome","Paris"])].reset_index()
ropa
d = distance.distance((ropa.loc[0, "lat"], ropa.loc[0, "lon"]), (ropa.loc[1, "lat"], ropa.loc[1, "lon"]))
d, d.km, d.miles

results = []
for f in [distance.distance, distance.great_circle, distance.geodesic]:
    for mes in ["kilometers","km","miles","mi","nautical","nm","feet","ft"]:
        d = f((ropa.loc[0, "lat"], ropa.loc[0, "lon"]), (ropa.loc[1, "lat"], ropa.loc[1, "lon"]))
        results.append({"method": f.__name__, "measurement": mes, "value": getattr(d, mes)})
results_df = pd.DataFrame(results)
print(results_df.pivot_table(index="method", columns="measurement", values="value"))
lon_1 = ropa.loc[0, "lon"]
lon_2 = ropa.loc[1, "lon"]
lat = ropa.loc[0, "lat"]
lat_2 = ropa.loc[1, "lat"]
r = requests.get(f"http://router.project-osrm.org/route/v1/car/{lon_1},{lat};{lon_2},{lat_2}?overview=false""")
# then you load the response using the json libray
# by default you get only one alternative so you access 0-th element of the `routes`
routes = json.loads(r.content)
route_1 = routes.get("routes")[0]

print("TOTAL SUM:",  calculate(5, 500, results[1]["value"]))

#cursor.execute("SELECT ord_status, COUNT(ord_status) FROM customers1 GROUP BY ord_status")

#myresult = cursor.fetchall()
#for x in myresult:
#  print(x)