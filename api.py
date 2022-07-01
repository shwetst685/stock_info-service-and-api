from flask import Flask
import sqlite3
from flask_restful import Api, Resource
import stock_info
import pandas as pd

connection = sqlite3.connect('stockData.db')
cur=connection.cursor()

df = pd.read_sql_query("""SELECT * FROM stocks""",connection)
curr_date=df["Date"][0]
prev_date=df["Date"][1]

def get_top_gainers():
    pass

def get_top_loosers():
    pass

def weekly_reports():
    pass


app = Flask(__name__)
api=Api(app)

class Reports(Resource):
    def get(self,report):
        if report =="get_top_gainers":
            return get_top_gainers()
        elif report =="get_top_loosers":
            return get_top_loosers()
        elif report =="weekly_reprots":
            return weekly_reports()

api.add_resource(Reports, "/reports/<string:report>")

if __name__ =="__main__":
    app.run(debug=False)

