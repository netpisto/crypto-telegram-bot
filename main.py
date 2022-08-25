from datetime import datetime
from time import sleep
from telegram import Bot
import pandas as pd
import pandas_ta as ta
from binance.client import Client

bot_id = input("bot http token : ")
channel_id = input("channel id : ")
def send_message(msg):
    global bot_id,channel_id
    bot = Bot(bot_id)
    print(datetime.now(),"bot :",msg)
    bot.send_message(text=msg,chat_id=channel_id)

send_message("Hello World")

client = Client()
pair = "BTCUSDT"
frame = "15m" # minute (best frame for day trading (for crypto))
ema_short = 5
ema_long = 20

def getminutedata(symbol,interval,lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback+" day ago UTC"))
    frame = frame.iloc[:,:6]
    frame.columns = ["Time","Open","High","Low","Close","Volume"]
    frame = frame.set_index("Time")
    frame.index = pd.to_datetime(frame.index,unit="ms")
    frame = frame.astype(float)
    frame = frame.Close.to_frame()
    return frame
buyed = None 
while True :
    sleep(15)
    df = getminutedata("BTCUSDT",frame,"1")
    
    df["EMA_SHORT"] = ta.ema(df.Close,ema_short)
    df["EMA_LONG"] = ta.ema(df.Close,ema_long)
    df.dropna(inplace=True)
    if df.EMA_SHORT.iloc[-2] > df.EMA_LONG.iloc[-2] and  buyed != True  :
        buyed = True 
        send_message("BTCUSDT : ema "+str(ema_short)+" is above the ema "+str(ema_long)+"in the "+frame+" time frame | take long position \n close : "+str(df.Close.iloc[-1])+"$")
    elif df.EMA_SHORT.iloc[-2] < df.EMA_LONG.iloc[-2] and buyed != False :
        buyed = False
        send_message("BTCUSDT : ema "+str(ema_short)+" is below the ema "+str(ema_long)+" in the "+frame+" time frame | take short position \n close : "+str(df.Close.iloc[-1])+"$")
    
