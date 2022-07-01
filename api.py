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
    new_df=df[["Ticker","Close"]][0:40]
    gainers_list=[]
    list = []
    for i in range(0,20):
        change=(new_df["Close"][i]-new_df["Close"][20+i])*100/(new_df["Close"][20+i])
        list.append(change)
    list2=sorted(list)
    for key,item in enumerate(list2):
        dict_ticker={}
        index=list.index(item)
        dict_ticker["rank"]=key
        dict_ticker["ticker"]=new_df["Ticker"][index]
        dict_ticker["change"]=list[index]

    return gainers_list[0:10]

def get_top_losers():
    new_df=df[["Ticker","Close"]][0:40]
    losers_list=[]
    list = []
    for i in range(0,20):
        change=(new_df["Close"][i]-new_df["Close"][20+i])*100/(new_df["Close"][20+i])
        list.append(change)
    list2=sorted(list,reverse=True)
    for key,item in enumerate(list2):
        dict_ticker={}
        index=list.index(item)
        dict_ticker["rank"]=key
        dict_ticker["ticker"]=new_df["Ticker"][index]
        dict_ticker["change"]=list[index]
        
    return losers_list[0:10]

def weekly_reports():
    week_dict = []
    for i in range(0,20):
        dict_ticker ={}
       
        rows = range(0+i,20*4+i,20)
        new_df =df[["Ticker","High","Low","Close"]][rows]
        dict_ticker["ticker"]=new_df["Ticker"][0]
        dict_ticker["high"]=new_df["High"].max()
        dict_ticker["low"]=new_df["Low"].min()
        dict_ticker["average"]=new_df["Close"].mean()

        week_dict.append(dict_ticker)
    return week_dict

app = Flask(__name__)
api=Api(app)

class Reports(Resource):
    def get(self,report):
        if report =="get_top_gainers":
            return get_top_gainers()
        elif report =="get_top_losers":
            return get_top_loosers()
        elif report =="generate_weekly_reprots":
            return weekly_reports()

api.add_resource(Reports, "/reports/<string:report>")

if __name__ =="__main__":
    app.run(debug=False)

