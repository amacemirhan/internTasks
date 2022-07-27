
from os import access
import requests
import json
import datetime
todo = {
  "email": "admin",
  "password": "admin"
}
r=requests.post("http://{ip:port}/api/internal/login",json=todo)
token=r.json()['jwt']
myDict = {

}
appData=requests.get("http://{ip:port}/api/devices?limit=15&applicationID=13",headers={"Grpc-Metadata-Authorization":token})
for i in range(int(appData.json()['totalCount'])):
   myDict[appData.json()['result'][i]['name']] = appData.json()['result'][i]['lastSeenAt']
for key in myDict:
    try:
        date_time_obj = datetime.datetime.strptime(myDict[key], '%Y-%m-%dT%X.%fZ')
        diff = datetime.datetime.now()-date_time_obj
        diff_in_hours = diff.total_seconds() / 3600
        if(diff_in_hours>2):
            print(key + " ->  {hour:.2f} hours ago".format(hour=diff_in_hours))
    except TypeError:
        print(key + " -> last time is unknown")
    



