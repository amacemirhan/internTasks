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

client = InfluxDBClient(host='{ip}',port=8086)

client.switch_database('{databaseName}')

querys = "SELECT time,value from {TableName} where dev_eui='{dev_eui}' and value < 100 order by time desc limit "+str(maxData)
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
with open('serialized_model.json', 'w') as fout:
    fout.write(model_to_json(m))  # Save model

# with open('serialized_model.json', 'r') as fin:
#     m = model_from_json(fin.read())  # Load model

future = m.make_future_dataframe(periods=predictDay)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)

plot_plotly(m, forecast)

plot_components_plotly(m, forecast)

# rslt_df = forecast[forecast.index>=0]
# rslt_df = rslt_df[['ds','yhat']]
# rslt_df = rslt_df.set_index(['ds'])
# rslt_df.to_csv(r'pandas.txt', header=None, index=True, sep=' ', mode='w')
# print(rslt_df)
dateTemp = forecast[['ds','yhat']]
dateTemp['ds'] = pd.to_datetime(dateTemp['ds']).dt.date
dateTemp = dateTemp.drop_duplicates(subset=['ds'],keep='last')
print(dateTemp)

dateTemp.to_csv(r'dateTemp.txt', header=True, index=True, sep=' ', mode='w')
yhat = dateTemp[['yhat']].to_numpy()

top = 0
many = 0
for i in range(len(yhat)):
    try:

        curDeg = yhat[i]-yhat[i+1]
        if(curDeg>0):
            top += curDeg
            many += 1
    except IndexError:
        break
avg = top/many
print(avg)
((1.1*avg)/100)*predictDay
print(str(((1.1*avg)/100)*predictDay)+" kilogram sabun gerekecek.")

plt.show()
