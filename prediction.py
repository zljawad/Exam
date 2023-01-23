import asyncio
import websockets
import pandas as pd
import numpy as np
import joblib
import time
import json
import random as rd
from datetime import datetime
import math
from kafka import KafkaProducer

# Use pd.read_csv to read the dataset. (The dataset is stored in the current directory so that it can be read directly.)
data=pd.read_csv('./ai4i2020.csv')

X=data.drop(['UDI', 'Product ID','TWF','HDF','PWF','OSF','RNF','Machine failure'],axis=1)


# Convert Categorical Variable to Numeric Variable
X['Type'].replace(['L', 'M', 'H'],
                        [0, 1, 2], inplace=True)

# After the dataset is split, standardize the data.
from sklearn.preprocessing import StandardScaler
std_scaler=StandardScaler().fit(X)

# input data


def aleatoire():
    processTemp = round(rd.uniform(300,320),2)
    airTemp = round(rd.uniform(290,300),2)
    rotationalSpeed = round(rd.uniform(1000,3000),0)
    torque = round(rd.uniform(20,80),2)
    toolWear = round(rd.uniform(0,300),0)
    list = [0, 1, 2]
    type1 = rd.choice(list)
    #print(type, processTemp, airTemp, rotationalSpeed, torque, toolWear)
    data = {"Type": type1,
            "Air temperature [K]":airTemp,
            "Process temperature [K]":processTemp,
            "Rotational speed [rpm]":rotationalSpeed,
            "Torque [Nm]":torque,
            "Tool wear [min]":toolWear} 
    return data

def serializer(message):
        return json.dumps(message).encode('utf-8')
  
#Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)


loadmodel=joblib.load('ai4i2020.pkl')

while True:
    data = [aleatoire() for i in range(4)]
    df = pd.DataFrame(data)
    # Data standardization 
    data_prediction = std_scaler.transform(df)

    resultatPrediction = loadmodel.predict(data_prediction)

    listPredictions = [int(resultatPrediction[i]) for i in range(4)]
   
    dic = json.dumps({"prediction":listPredictions,"data":data[0]})

    print(dic)
    producer.send('test', dic)  

    time.sleep(3)


