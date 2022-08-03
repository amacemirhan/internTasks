from email import header
from operator import index
from influxdb import InfluxDBClient
import influxdb_client as cl
import json
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import numpy as np
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.offline as py
import datetime
from prophet.serialize import model_to_json, model_from_json
import numpy

maxData = 100000
predictDay = 30
maxSensorDeger = 100

client = InfluxDBClient(host='37.148.212.112',port=8086)

client.switch_database('loradb')

querys = "SELECT time,value from device_frmpayload_data_FacilityMan where dev_eui='4f9d9d06c06f320a' and value < 100 order by time desc limit "+str(maxData)
result = client.query(querys)
df = pd.DataFrame.from_dict(result.raw["series"][0]['values'])
df['Datetime'] = pd.to_datetime(df[0])
df['ds']=df['Datetime'].dt.tz_localize(None)

del df[0]
del df['Datetime']
df["y"]=df[1]
del df[1]

print(df)

m = Prophet()
m.fit(df)

future = m.make_future_dataframe(periods=predictDay)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)

plot_plotly(m, forecast)

plot_components_plotly(m, forecast)

dateTemp = forecast[['ds','yhat']]
dateTemp['ds'] = pd.to_datetime(dateTemp['ds']).dt.date

dateTemp = dateTemp.drop_duplicates(subset=['ds'],keep='last')
print(dateTemp)

yhat = dateTemp[['yhat']].to_numpy()

# top = 0
# many = 0
# for i in range(len(yhat)):
#     try:

#         curDeg = yhat[i]-yhat[i+1]
#         if(curDeg>0):
#             top += curDeg
#             many += 1
#     except IndexError:
#         break
#avg = top/many #yapilan gozlemler sonucu ort azalmanın bir gunde %23 oldugu tahmin edildi
avg = 23
((1.1*avg)/maxSensorDeger)*predictDay
report = "Gelecek "+str(predictDay)+" gün için "+str(((1.1*avg)/maxSensorDeger)*predictDay)+" kilogram sabun gerekecek."
print(report)
file = open("rapor.txt", "w")
file.write(report)
dateTemp['kg']=(dateTemp['yhat']*1.1)/maxSensorDeger
file.write('''Günler ve yüzdelik sabun seviyelerini excel dosyasında bulabilirsiniz.\n
ds sütunu o gün sabunlukların yüzdelik cinsinden gönderdikleri sabun miktarının\n
yüzde kaç olduğunu, kg sütunu ise kaç kilograma denk geldiği bilgisidir. 
''')
dateTemp.to_excel('DaysWithSoap.xlsx', index=False)

file.close()

plt.show()