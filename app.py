import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import forecast as f
from flask_bootstrap import Bootstrap


df = pd.read_csv(os.getcwd() + os.path.sep + "Beverage.csv")
df = f.preprocess_data(df)

time = df.index.tolist()
blower_data = df["Blower"].tolist()
labeller_data = df["Labeller"].tolist()

app = Flask(__name__)
Bootstrap(app)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blower")
def blower():
    times = time
    legend = "Blower Values"
    b_data = blower_data
    return render_template("blower.html", values=b_data, labels=times, legend=legend)

@app.route("/blower_predict", methods=['POST'])
def blower_predict():
    #times = time
    legend = "Blower Values"
    b_data = blower_data
    
    equipment_name = 'Blower'
    forecast_time = int(request.form['input_forecast'])
    forecast_df = f.forecast(df, equipment_name, forecast_time)
    
    p_legend = "Predicted Values"
    p_time = forecast_df.index.tolist()
    p_blower_data = forecast_df["Blower Forecast"].tolist()
    
    
    return render_template("blower.html", 
                           values=b_data, 
                           labels=p_time, 
                           legend=legend, 
                           tables=[forecast_df.to_html(classes='forecast_df')],
                           p_legend=p_legend,
                           p_blower_data=p_blower_data)

@app.route("/labeller")
def labeller():
    times = time
    legend = "Labeller Values"
    l_data = labeller_data    
    return render_template("labeller.html", values=l_data, labels=times, legend=legend)

@app.route("/labeller_predict", methods=['POST'])
def labeller_predict():
    #times = time
    legend = "Labeller Values"
    l_data = labeller_data
    
    equipment_name = 'Labeller'
    forecast_time = int(request.form['input_forecast'])
    forecast_df = f.forecast(df, equipment_name, forecast_time)
    
    p_legend = "Predicted Values"
    p_time = forecast_df.index.tolist()
    p_labeller_data = forecast_df["Labeller Forecast"].tolist()
    
    return render_template("labeller.html", 
                           values=l_data, 
                           labels=p_time, 
                           legend=legend, 
                           tables=[forecast_df.to_html(classes='forecast_df')],
                           p_legend=p_legend,
                           p_labeller_data=p_labeller_data)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()