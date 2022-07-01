import sqlite3
import pandas as pd
import uuid
import yfinance as yf
from datetime import  datetime,time,date
import random
from pathlib import Path
from check import SMWinservice

# function to fetch the data from yahoo finance api and store the data in sqlite local database
def stockInfo():
    connection = sqlite3.connect('stockData.db')
    cur=connection.cursor()

    df1 = pd.read_csv('ticker_symbols.txt', sep=" ") # ticker symbols file containing ticker names

    # check if table exixts already, if not create a new table
    listOfTables = cur.execute("""SELECT name FROM sqlite_master WHERE type='table' """).fetchall()
    
    if listOfTables == []:
        cur.execute('''CREATE TABLE stocks (id, DATE, NAME, TICKER, HIGH, LOW, CLOSE)''') 

    #for each ticker pull data and store into sqlite database
    for ticker in df1["stock"]:
        ticker1=yf.Ticker(ticker)
        data=ticker1.history(period='1d')
        latest_date=str(data.index[0]).split(" ")[0]
        id = str(uuid.uuid1())
        cur.execute("""INSERT INTO stocks (id, DATE, STOCK,TICKER,HIGH,LOW,CLOSE) VALUES (?,?,?,?,?,?,?)""",(id, latest_date,ticker1.info["longName"],ticker,data["High"][0],data["Low"][0],data["Close"][0]))

    #subclass from check file to run the script as windows service
class stock_market(SMWinservice):
    _svc_name_ = "StockService"
    _svc_display_name_ = "Stock Service"
    _svc_description_ = "Stock market info"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        i = 0
        while self.isrunning:
            stockInfo()
            time.sleep(5)

if __name__ == '__main__':
    stock_market.parse_command_line()



