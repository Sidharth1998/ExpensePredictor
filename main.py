from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash

import json
import pandas as pd
import io
from flask import make_response
from forecast import *

## Reading the data and predicting the values
df = pd.read_csv('https://github.com/Sidharth1998/ExpensePredictor/blob/main/BLS_Data.csv', sep=",")
df = clean_data(df)
forecast_values = forecasting(df)
forecast_values['date'] = forecast_values['date'].apply(lambda x: pd.to_datetime(x).strftime("%b %Y"))
forecast_values['item_name'] = forecast_values.index
app = Flask(__name__)

@app.route('/')
def index():
    items = list(set(df.index))
    dates = list(forecast_values['date'].unique()[-4:])
    # print(dates)
    # dates = [pd.to_datetime(date).strftime("%b %Y") for date in dates]
    return render_template('main.html', items=items, dates = dates, prices = forecast_values)

@app.route('/GroceryExpense', methods=['GET', 'POST'])
def groceryExpense():
    items = list(set(df.index))
    # Quantity user selected
    quantity = {}
    # Creating total amount for the forecasted months
    final_amounts = {}
    # Get dates
    dates = list(forecast_values['date'].unique()[-4:])
    # dates = [pd.to_datetime(date).strftime("%b %Y") for date in dates]

    # Total for each forecast month
    total_expense = {}

    if request.method == 'POST':
        for item in items:
            quantity[item] = int(request.form.get(item))
        
        for item in items:
            final_amounts[item] = {}
            data = forecast_values[forecast_values.item_name == item].tail(4)
            for date in dates:
                final_amounts[item][date] = quantity[item] * data['price'][dates.index(date)]
                total_expense[date] = 0
        
        for _, val in final_amounts.items():
            for date, cost in val.items():
                total_expense[date] += cost
    
    return render_template('expense.html', items=items, dates = dates, quantity = quantity, monthly_cost = final_amounts, total = total_expense)
