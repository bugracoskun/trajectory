import requests
import psycopg2

try:
    f = open("database.txt", "r")
    database=f.readline().rstrip("\n")
    user=f.readline().rstrip("\n")
    password=f.readline().rstrip("\n")
    host=f.readline().rstrip("\n")
    port=f.readline().rstrip("\n")
    appid=f.readline().rstrip("\n")
    conn = psycopg2.connect(database=database,
                        user=user,
                        password=password,
                        host=host,
                        port=port)

    print("Successfully Connected")
except:
    print("Connection failed")



f2 = open("trajectory_ships_20min_v2.txt", "r")
for x in f2:
    line=x.split()
    print(line)



'''
url="http://history.openweathermap.org/data/2.5/history/city?lat="+str(30)+"&lon="+str(30)+"&start="+"1607547600"+"&end="+"1607547600"+"&appid="+appid

response = requests.get(url)
print(response.status_code, response.reason)
print(response.text)
'''

