from flask import Flask, render_template, request
import sklearn
import pandas as pd
from datetime import datetime
import pickle
import numpy as np

filename = 'fare_price_model.pkl'
regressor = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=["GET", "POST"])
def predict():
    temp=list()
    if request.method == 'POST':


        #Total Stop
        Stopage=int(request.form["Stopage"])
        temp=temp+[Stopage]

        #Airline
        Airline=request.form["Airline"]
        if Airline == 'Air India':
            temp = temp + [1,0,0,0,0,0,0,0,0,0,0]
        elif Airline == 'Vistara Premium economy': 
            temp = temp + [0,1,0,0,0,0,0,0,0,0,0]
        elif Airline == 'Trujet':
            temp = temp + [0,0,1,0,0,0,0,0,0,0,0]
        elif Airline == 'GoAir':
            temp = temp + [0,0,0,1,0,0,0,0,0,0,0]
        elif Airline == 'IndiGo':
            temp = temp + [0,0,0,0,1,0,0,0,0,0,0]
        elif Airline == 'Jet Airways':
            temp = temp + [0,0,0,0,0,1,0,0,0,0,0]
        elif Airline == 'Jet Airways Business':
            temp = temp + [0,0,0,0,0,0,1,0,0,0,0]
        elif Airline == 'Multiple carriers':
            temp = temp + [0,0,0,0,0,0,0,1,0,0,0]
        elif Airline == 'Multiple carriers Premium economy':
            temp = temp + [0,0,0,0,0,0,0,0,1,0,0]
        elif Airline == 'SpiceJet':
            temp = temp + [0,0,0,0,0,0,0,0,0,1,0]
        elif Airline == 'Vistara':
            temp = temp + [0,0,0,0,0,0,0,0,0,0,1]
        else:
            temp = temp + [0,0,0,0,0,0,0,0,0,0,0]		

            #Source
        Source=request.form["Source"]
        if Source=="Chennai":
            temp=temp+[1,0,0,0]
        elif Source=="Delhi":
            temp=temp+[0,1,0,0]
        elif Source=="Kolkata":
            temp=temp+[0,0,1,0]
        elif Source=="Mumbai":
            temp=temp+[0,0,0,1]
        else:
            temp=temp+[0,0,0,0]

            #Destination
        Destination=request.form["Destination"]
        if Destination=="Cochin":
            temp=temp+[1,0,0,0,0]
        elif Destination=="Delhi":
            temp=temp+[0,1,0,0,0]
        elif Destination=="Hyderabad":
            temp=temp+[0,0,1,0,0]
        elif Destination=="Kolkata":
            temp=temp+[0,0,0,1,0]
        elif Destination=="New Delhi":
            temp=temp+[0,0,0,0,1]
        else:
            temp=temp+[0,0,0,0,0]

        #departure
        checkin=request.form['check-in']
        Journey_day = int(pd.to_datetime(checkin, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(checkin, format="%Y-%m-%dT%H:%M").month)
        Journey_year = int(pd.to_datetime(checkin, format="%Y-%m-%dT%H:%M").year)
        Dep_hour = int(pd.to_datetime(checkin, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(checkin, format="%Y-%m-%dT%H:%M").minute)

        temp=temp+[Journey_day,Journey_month,Dep_hour,Dep_min]

        #Arrival
        checkout=request.form['check-out']
        Arrival_day = int(pd.to_datetime(checkout, format="%Y-%m-%dT%H:%M").day)
        Arrival_month = int(pd.to_datetime(checkout, format="%Y-%m-%dT%H:%M").month)
        Arrival_year = int(pd.to_datetime(checkout, format="%Y-%m-%dT%H:%M").year)
        Arrival_hour = int(pd.to_datetime(checkout, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(checkout, format="%Y-%m-%dT%H:%M").minute)

        #Duration
        val1=datetime(Journey_year,Journey_month,Journey_day,Dep_hour,Dep_min,0)
        val2=datetime(Arrival_year,Arrival_month,Arrival_day,Arrival_hour,Arrival_min,0)

        Duration_hours=int(((val2-val1).total_seconds())/60**2)
        Duration_mins=int((((val2-val1).total_seconds())/60)%60)

        temp=temp+[Arrival_hour,Arrival_min,Duration_hours,Duration_mins]

        data = np.array([temp])
        my_prediction = int(regressor.predict(data)[0])
    return render_template("index.html",output=f'Predicted price is Rs. {my_prediction} ')

if __name__ == '__main__':
    app.run(debug=True)
