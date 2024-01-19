#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, datetime, os, sys, pandas, requests, subprocess, btalib, sched, ta, math
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
#from win10toast import ToastNotifier
from os import system as cmd
from binance.client import Client
import pandas_datareader.data as web
import urllib.request
from btalib import ema, macd
import pandas as pd
from pandas import DataFrame as df
import os.path
from bitmex import bitmex
from datetime import timedelta
from dateutil import parser
from tqdm import tqdm_notebook #(Optional, used for progress-bars)


def notifier(baslik="Bildirim",message="Mesaj Yok",time_second=5): #notifier
    #toast = ToastNotifier()
    #toast.show_toast(baslik,message,icon_path=r"C:/Users/HP/Desktop/VOIP/mm.ico",duration=time_second)
    print(baslik,message,time_second)
    return 


btmex_id = '0' #Enter your own API-key here
btmex_key = '0' #Enter your own API-secret here
client_id = ''
secret_key = ''
client = Client(client_id,secret_key)
def current_data_receiver(symbol="BTCUSDT",pys="SPOT"):
    if pys == "SPOT" or pys == "MARGIN":
        tickers = client.get_ticker()
        for i in range(len(tickers)):
            if tickers[i]['symbol'] == symbol:
                sembol = tickers[i]['symbol']
                fiyat_delta = tickers[i]['priceChange']
                fiyat_delta_percantage = tickers[i]['priceChangePercent']
                agirlikli_ortalama_fiyat = tickers[i]['weightedAvgPrice']
                onceki_kapanis_fiyati = tickers[i]['prevClosePrice'] 
                son_fiyat = float(tickers[i]['lastPrice'])
                lastQty= tickers[i]['lastQty']
                satis_fiyati = tickers[i]['bidPrice']
                satis_adeti = tickers[i]['bidQty']
                alis_fiyati = tickers[i]['askPrice']
                alis_adeti = tickers[i]['askQty'] 
                acilis_fiyati = tickers[i]['openPrice']
                top_fiyat = tickers[i]['highPrice']
                low_fiyat = tickers[i]['lowPrice']
                hacim = tickers[i]['volume']
                emir_hacmi = tickers[i]['quoteVolume']
                acilis_zamani = tickers[i]['openTime']
                kapanis_zamani= tickers[i]['closeTime']
                fi = tickers[i]['firstId']
                li = tickers[i]['lastId']
                count = tickers[i]['count']
                return sembol, fiyat_delta,fiyat_delta_percantage,agirlikli_ortalama_fiyat,onceki_kapanis_fiyati,son_fiyat,lastQty,satis_fiyati,satis_adeti,alis_fiyati,alis_adeti,acilis_fiyati,top_fiyat,low_fiyat,hacim,emir_hacmi,acilis_zamani,kapanis_zamani,fi,li,count
    if pys == "FUTURE" or pys == "FUTURE-SIM":
        tickers = client.futures_ticker()
        for i in range(len(tickers)):
            if tickers[i]['symbol'] == symbol:
                sembol = tickers[i]['symbol']
                fiyat_delta = tickers[i]['priceChange']
                fiyat_delta_percantage = tickers[i]['priceChangePercent']
                agirlikli_ortalama_fiyat = tickers[i]['weightedAvgPrice']
                onceki_kapanis_fiyati = 'non'
                son_fiyat = float(tickers[i]['lastPrice'])
                lastQty= tickers[i]['lastQty']
                satis_fiyati = 'non'
                satis_adeti = 'non'
                alis_fiyati = 'non'
                alis_adeti = 'non'
                acilis_fiyati = tickers[i]['openPrice']
                top_fiyat = tickers[i]['highPrice']
                low_fiyat = tickers[i]['lowPrice']
                hacim = tickers[i]['volume']
                emir_hacmi = tickers[i]['quoteVolume']
                acilis_zamani = tickers[i]['openTime']
                kapanis_zamani= tickers[i]['closeTime']
                fi = tickers[i]['firstId']
                li = tickers[i]['lastId']
                count = tickers[i]['count']
                return sembol, fiyat_delta,fiyat_delta_percantage,agirlikli_ortalama_fiyat,onceki_kapanis_fiyati,son_fiyat,lastQty,satis_fiyati,satis_adeti,alis_fiyati,alis_adeti,acilis_fiyati,top_fiyat,low_fiyat,hacim,emir_hacmi,acilis_zamani,kapanis_zamani,fi,li,count
    return


def grn_futures_asset(client_id, secret_key, symbol= 'USDT'):
    client = Client(client_id, secret_key)
    b = client.futures_account_balance()
    for i in range(len(b)):
        if b[i]['asset'] == symbol:
            return b[i]['balance']

def buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key):
    f = open('trade_log', "a")
    signal = "Alış Sinyali"
    monitor = ("Sinyal Tipi:{} \nSembol Adı:{} \nGiriş Tarihi:{} \nGiriş Fiyatı:{}".format(signal, sembol, datetime.datetime.now().strftime("%H:%M:%S"), price))
    #notifier("SİSTEM MESAJI",monitor,10)
    f.write("{0} -- {1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), monitor))
    f.close()
    grn_futures_asset(client_id, secret_key, sembol)
    if piyasa =='FUTURE-SIM':
        fi = open('{}lastprice_sim.txt'.format(sembol), "a")
        fi.write("\n")
        fi.write(str(price))
        fi.close()
        s = open('{}pos.txt'.format(sembol), "a")
        s.write("\n")
        s.write(str('10'))
        s.close()
    if piyasa == 'SPOT' and order_type == 'LIMIT':
        try:    
            client.order_limit_buy(symbol=sembol,quantity=quantityusr_first,price=price)
        except:
            print("passing...")
            notifier("SİSTEM MESAJI","BAĞLANTI HATASI",5)
            sw = True
            while sw == True:
                if connect() == True:
                    sw = False
                    print("connected")
                else:
                    time.sleep(20)
                    print("sleep 10")
                    continue 
            client.order_limit_buy(symbol=sembol,quantity=quantityusr_first,price=price)
            print("Order Succesfully Send...",datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    if piyasa == 'SPOT' and order_type == 'MARKET':
        client.order_market_buy(symbol=sembol, quantity=quantityusr_first)            
    if piyasa == 'FUTURE' and order_type == 'LIMIT':
        try:
            client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_LIMIT,quantity=quantityusr_first,timeInforce=client.TIME_IN_FORCE_GTC,price=price)
        except:
            print("order buy passing...")
            notifier("SİSTEM MESAJI","BAĞLANTI HATASI",5)
            sw = True
            while sw == True:
                if connect() == True:
                    sw = False
                    print("order buy connected")
                else:
                    time.sleep(20)
                    print("order buy sleep 10")
                    continue
            client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_LIMIT,quantity=quantityusr_first,timeInforce=client.TIME_IN_FORCE_GTC,price=price) 
    if piyasa == 'FUTURE' and order_type == 'MARKET':
        try:    
            client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_MARKET,quantity=quantityusr_first)
        except:
            print("passing...")
            notifier("SİSTEM MESAJI","BAĞLANTI HATASI",5)
            sw = True
            while sw == True:
                if connect() == True:
                    sw = False
                    print("+connected")
                else:
                    time.sleep(20)
                    print("sleep 10")
                    continue 
            client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_MARKET,quantity=quantityusr_first)
            print("Order Succesfully Send...",datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    return 

def sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key):
    f = open('trade_log', "a")
    signal = "Satış Sinyali"
    monitor = ("Sinyal Tipi: {} \nSembol Adı:{} \nGiriş Tarihi:{} \nGiriş Fiyatı:{}".format(signal, sembol, datetime.datetime.now().strftime("%H:%M:%S"), price))
    f.write("{0} -- {1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), monitor))
    #notifier("SİSTEM MESAJI",monitor,5)
    f.close()
    n = grn_futures_asset(client_id, secret_key, sembol)
    if piyasa =='FUTURE-SIM':
        fi = open('{}lastprice_sim.txt'.format(sembol), "a")
        fi.write("\n")
        fi.write(str(price))
        fi.close()
        s = open('{}pos.txt'.format(sembol), "a")
        s.write("\n")
        s.write(str('-10'))
        s.close()
    if piyasa == 'SPOT' and order_type == 'LIMIT':
        try:
            client.order_limit_sell(symbol=sembol,quantity=quantityusr_2nd,price=price)
        except:
            print("passing...")
            notifier("SİSTEM MESAJI","BAĞLANTI HATASI",5)
            sw = True
            while sw == True:
                if connect() == True:
                    sw = False
                    print("connected")
                else:
                    time.sleep(20)
                    print("sleep 10")
                    continue 
            client.order_limit_sell(symbol=sembol,quantity=quantityusr_2nd,price=price)
            print("Order Succesfully Send...",datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    if piyasa == 'SPOT' and order_type == 'MARKET':
        client.order_market_sell(symbol=sembol, quantity=quantityusr_2nd)
    if piyasa == 'FUTURE' and order_type == 'LIMIT':
        try:
            client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_LIMIT,quantity=quantityusr_first,timeInforce=client.TIME_IN_FORCE_GTC,price=price)
        except:
            print("order buy passing...")
            notifier("SİSTEM MESAJI","BAĞLANTI HATASI",5)
            sw = True
            while sw == True:
                if connect() == True:
                    sw = False
                    print("order sell connected")
                else:
                    time.sleep(20)
                    print("order sell sleep 10")
                    continue
            client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_LIMIT,quantity=quantityusr_first,timeInforce=client.TIME_IN_FORCE_GTC,price=price) 
    if piyasa == 'FUTURE' and order_type == 'MARKET':
        try:    
            client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_MARKET,quantity=quantityusr_first)
        except:
            print("passing...")
            notifier("SİSTEM MESAJI","BAĞLANTI HATASI",5)
            sw = True
            while sw == True:
                if connect() == True:
                    sw = False
                    print("connected")
                else:
                    time.sleep(20)
                    print("sleep 10")
                    continue 
            client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_MARKET,quantity=quantityusr_first)
            print("Order Succesfully Send...",datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))                                
    return 
        
def historic_dr(symbol='ATOMUSDT', kline_size='1d', save = False):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
    #delta_min = (newest_point - oldest_point).total_seconds()/60
    #available_data = math.ceil(delta_min/binsizes[kline_size])
    #if oldest_point == datetime.strptime('20 Sep 2020', '%d %b %Y'): print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    #else: print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"),newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save: data_df.to_csv(filename)
    #rint('All caught up..!')
    return data_df

def receiver(symbol='ATOMUSDT',start_time="2020-11-22 16:00:00",end_time=datetime.datetime.now()):
    client = Client(client_id, secret_key)
    agg_trades = client.aggregate_trade_iter(symbol, start_time)
    # iterate over the trade iterator
    for trade in agg_trades:
        dt_object = time.strftime('%Y-%m-%d %H:%M:%S,',  time.gmtime(trade['T']/1000.))
        print(dt_object,trade)
        # do something with the trade data


### API
bitmex_api_key = btmex_id   #Enter your own API-key here
bitmex_api_secret = btmex_key #Enter your own API-secret here
binance_api_key = client_id    #Enter your own API-key here
binance_api_secret = secret_key #Enter your own API-secret here


### CONSTANTS
binsizes = {"1s":1,"1m": 1,"3m": 1, "5m": 5, "15m": 15, "1h": 60, "1d": 1440}
batch_size = 750
bitmex_client = bitmex(test=False, api_key=bitmex_api_key, api_secret=bitmex_api_secret)
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:  old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance": old = datetime.datetime.strptime('18 Oct 2020', '%d %b %Y')
    elif source == "bitmex": old = bitmex_client.Trade.Trade_getBucketed(symbol=symbol, binSize=kline_size, count=1, reverse=False).result()[0][0]['timestamp']
    if source == "binance": new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    if source == "bitmex": new = bitmex_client.Trade.Trade_getBucketed(symbol=symbol, binSize=kline_size, count=1, reverse=True).result()[0][0]['timestamp']
    return old, new

def get_all_binance(symbol, kline_size, save = False,pysn='SPOT'):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
    #delta_min = (newest_point - oldest_point).total_seconds()/60
    #available_data = math.ceil(delta_min/binsizes[kline_size])
    #if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'): print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    #else: print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    if pysn == 'SPOT' or pysn == 'MARGIN':
        filename = '%s-%s-data.csv' % (symbol, kline_size)
        if os.path.isfile(filename): data_df = pd.read_csv(filename)
        else: data_df = pd.DataFrame()
        oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
        klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
        data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        if len(data_df) > 0:
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
        else: data_df = data
        data_df.set_index('timestamp', inplace=True)
        if save: data_df.to_csv(filename)
        #print('All caught up..!')
        return data_df
    if pysn == 'FUTURE' or pysn == 'FUTURE-SIM':
        filename = '%s-FUTURE-%s-data.csv' % (symbol, kline_size)
        if os.path.isfile(filename): data_df = pd.read_csv(filename)
        else: data_df = pd.DataFrame()
        oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
        klines = binance_client.futures_klines(symbol=symbol, interval=kline_size,startTime=oldest_point.strftime("%d %b %Y %H:%M:%S"),endTime=newest_point.strftime("%d %b %Y %H:%M:%S"))
        data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        if len(data_df) > 0:
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
        else: data_df = data
        data_df.set_index('timestamp', inplace=True)
        if save: data_df.to_csv(filename)
        #print('All caught up..!')
        return data_df
    #binance_symbols = ["BTCUSDT", "ETHBTC", "XRPBTC","ATOMUSDT","NEOUSDT","QTUMUSDT","IOSTUSDT","THETAUSDT","ALGOUSDT","ZILUSDT","KNCUSDT","ZRXUST","COMPUSDT","OMGUSDT","DOGEUSDT","SXPUSDT","KAVAUSDT","BANUSDT","RLCUSDT","WAVEUSDT","MKRUSDT","SNXUSDT","DOTUSDT","DEFIUSDT","YFIUSDT"]
    #for symbol in binance_symbols:
        #get_all_binance(symbol, '5m', save = True)

def get_all_bitmex(symbol, kline_size, save = False):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "bitmex")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    rounds = math.ceil(available_data / batch_size)
    if rounds > 0:
        print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data in %d rounds.' % (delta_min, symbol, available_data, kline_size, rounds))
        for round_num in tqdm_notebook(range(rounds)):
            time.sleep(1)
            new_time = (oldest_point + timedelta(minutes = round_num * batch_size * binsizes[kline_size]))
            data = bitmex_client.Trade.Trade_getBucketed(symbol=symbol, binSize=kline_size, count=batch_size, startTime = new_time).result()[0]
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
    data_df.set_index('timestamp', inplace=True)
    if save and rounds > 0: data_df.to_csv(filename)
    #print('All caught up..!')
    return data_df

def yess_rf_heinekenashi(symbol, perM, per, mult,pys='SPOT'):
        #Settings for 5min chart, BTCUSDC. For Other coin, change the paremeters
        #src ; kaynak // açılış, kapanış,yüksek,düşük,hl2,ydk3, ohlc4, Pmax:Moving AVerage Line, Pmax:Pmax, Pmax:, Hacim:VOlume, Hacim:Volume MA, RSI // yazı girdisi
        #per ; sample periyodu // sayı girdisi #1 den küçük olamaz !!!!!
        #mult ; range çarpıcı 0.1 den küçük olmaz !!!

    def smoothrng(src, per, mult): #smoothrng(x, t, m)=>
        wper = (per*2) - 1
        avrng = ta.trend.ema_indicator(abs(src.diff()), per)
        pd.options.display.float_format = '{:.3f}'.format
        smoothrng = ta.trend.ema_indicator(avrng, wper) * mult
        return smoothrng
        
        # x[1] 1 gün öncesinin close değeri 
        # x son close değeri 
    
    def nz(val):
        if val == "NaN":
            s = 0
        else:
            s = val
        return s
        
    def rangefilter(x, r):     
        if (x.iloc[-1] > nz(x.iloc[-2])):
            if ((x.iloc[-1] - r.iloc[-1]) < nz(x.iloc[-2])):
                rngfilt = nz(x.iloc[-2])
            else:
                rngfilt = (x.iloc[-1] - r.iloc[-1])
        else:
            if ((x.iloc[-1] + r.iloc[-1]) > nz(x.iloc[-2])):
                rngfilt = nz(x.iloc[-2])
            else:
                rngfilt = (x.iloc[-1] + r.iloc[-1])
        return rngfilt
    
    get_all_binance(symbol, perM, save = True, pysn=pys)

    if pys == 'SPOT' or pys == 'MARGIN':
        btc_df = pd.read_csv('{}-{}-data.csv'.format(symbol,perM), index_col=0)
    if pys == 'FUTURE':
        btc_df = pd.read_csv('{}-{}-{}-data.csv'.format(symbol,'FUTURE',perM), index_col=0)
    if pys == 'FUTURE-SIM':
        btc_df = pd.read_csv('{}-{}-{}-data.csv'.format(symbol,'FUTURE',perM), index_col=0)
    
    src = (btc_df['close']+btc_df['open']+btc_df['high']+btc_df['low'])/4
    src2 = (btc_df['close'].iloc[:-1] + +btc_df['open'].iloc[:-1]+btc_df['high'].iloc[:-1]+btc_df['low'].iloc[:-1])/4
    smrng = smoothrng(src, per, mult)
    filt_1 = rangefilter(src2, smrng)
    filt_2 = rangefilter(src, smrng)
    
    upward = 0.0
    downward = 0.0

    if (filt_2 > filt_1):
        upward = nz(upward) + 1
    if (filt_2 < filt_1):
        upward = 0
    else:
        upward = nz(upward)


    if (filt_2 < filt_1):
        downward = nz(downward) + 1
    if (filt_2 > filt_1):
        downward = 0
    else:
        downward = nz(downward)      
    
    
    #break outs
    longCond = False
    shortCond = False
    
    if ((src.iloc[-1] > filt_2) and (src.iloc[-1] > src.iloc[-2]) and (upward > 0)) or ((src.iloc[-1] > filt_2) and (src.iloc[-1] < src.iloc[-2]) and (upward > 0)): 
        longCond = True 
    
    if ((src.iloc[-1] < filt_2) and (src.iloc[-1] < src.iloc[-2]) and (downward > 0)) or ((src.iloc[-1] < filt_2) and (src.iloc[-1] > src.iloc[-2]) and (downward > 0)): 
        shortCond = True 
    
    CondIni = 0

    if longCond == True:
        CondIni = 1
    if longCond == False:
        if shortCond == True:
            CondIni = -1
    if pys == 'SPOT' or pys == 'MARGIN':
        fileHandle = open ( './{}signals{}.txt'.format(symbol,perM),"r" )
        lineList = fileHandle.readlines()
        fileHandle.close()
        
        try:
            prev_val = lineList[-1]
        except:
            prev_val = 'NON'

        f1=open('./{}signals{}.txt'.format(symbol,perM), 'a')
        signaling = 0
        
        if longCond == True and CondIni == 1:
            signaling = "AL"
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

                f1.close()
                return signaling
        
        if shortCond == True and CondIni == -1:
            signaling = "SAT"
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

                f1.close()
                return signaling
        f1.close()
        
        os.remove('{}-{}-data.csv'.format(symbol,perM))
    if pys == 'FUTURE':
        filename = ('./{}-{}-signals{}.txt'.format(symbol,pys,perM))
        file_exists = os.path.isfile(filename) 
        
        if file_exists:
            file = open(filename,"a+" )
            file.close()
        else:
            fileHandle = open ( './{}-{}-signals{}.txt'.format(symbol,pys,perM),"a" )
            fileHandle.close()
        fileHandle = open ( './{}-{}-signals{}.txt'.format(symbol,pys,perM),"r" )
        lineList = fileHandle.readlines()
        fileHandle.close()
        try:
            prev_val = lineList[-1]
        except:
            prev_val = 'NON'

        f1=open('./{}-{}-signals{}.txt'.format(symbol,pys,perM), 'a')
        signaling = 0
        
        if longCond == True and CondIni == 1:
            signaling = "AL"
            
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

            f1.close()
            return signaling

        
        if shortCond == True and CondIni == -1:
            signaling = "SAT"

            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

            f1.close()
            return signaling

        else:
            f1.write("\n")
            f1.write('non')
            f1.close()
            return 'non'

        f1.close()
        
        #os.remove('{}-FUTURE-{}-data.csv'.format(symbol,perM))
    if pys == 'FUTURE-SIM':
        filename = ('./{}-FUTURE-signals{}.txt'.format(symbol,perM))
        file_exists = os.path.isfile(filename) 
        
        if file_exists:
            file = open(filename,"a+" )
            file.close()
        else:
            fileHandle = open ( './{}-FUTURE-signals{}.txt'.format(symbol,perM),"a" )
            fileHandle.close()

        fileHandle = open ( './{}-FUTURE-signals{}.txt'.format(symbol,perM),"r" )
        lineList = fileHandle.readlines()
        fileHandle.close()
        try:
            prev_val = lineList[-1]
        except:
            prev_val = 'NON'
        f1=open('./{}-FUTURE-signals{}.txt'.format(symbol,perM), 'a')
        signaling = 0
        
        if longCond == True and CondIni == 1:
            signaling = "AL"
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

                f1.close()
                
                return signaling
        
        if shortCond == True and CondIni == -1:
            signaling = "SAT"
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

                f1.close()
                
                return signaling
        f1.close()
        
        os.remove('{}-FUTURE-{}-data.csv'.format(symbol,perM))
    return 

def ema_f(symbol,perM,per):
    get_all_binance(symbol, perM, save = True)
    btc_df = pd.read_csv('{}-{}-data.csv'.format(symbol,perM), index_col=0)
    src = btc_df['close']
    return ta.trend.ema_indicator(src, per)

def yess_rf_v2(symbol, perM, per, mult,pys='SPOT'):
        #Settings for 5min chart, BTCUSDC. For Other coin, change the paremeters
        #src ; kaynak // açılış, kapanış,yüksek,düşük,hl2,ydk3, ohlc4, Pmax:Moving AVerage Line, Pmax:Pmax, Pmax:, Hacim:VOlume, Hacim:Volume MA, RSI // yazı girdisi
        #per ; sample periyodu // sayı girdisi #1 den küçük olamaz !!!!!
        #mult ; range çarpıcı 0.1 den küçük olmaz !!!

    def smoothrng(src, per, mult): #smoothrng(x, t, m)=>
        wper = (per*2) - 1
        avrng = ta.trend.ema_indicator(abs(src.diff()), per)
        pd.options.display.float_format = '{:.3f}'.format
        smoothrng = ta.trend.ema_indicator(avrng, wper) * mult
        return smoothrng
        
        # x[1] 1 gün öncesinin close değeri 
        # x son close değeri 
    
    def nz(val):
        if val == "NaN":
            s = 0
        else:
            s = val
        return s
        
    def rangefilter(x, r):     
        if (x.iloc[-1] > nz(x.iloc[-2])):
            if ((x.iloc[-1] - r.iloc[-1]) < nz(x.iloc[-2])):
                rngfilt = nz(x.iloc[-2])
            else:
                rngfilt = (x.iloc[-1] - r.iloc[-1])
        else:
            if ((x.iloc[-1] + r.iloc[-1]) > nz(x.iloc[-2])):
                rngfilt = nz(x.iloc[-2])
            else:
                rngfilt = (x.iloc[-1] + r.iloc[-1])
        return rngfilt
    
    get_all_binance(symbol, perM, save = True, pysn=pys)

    if pys == 'SPOT' or pys == 'MARGIN':
        btc_df = pd.read_csv('{}-{}-data.csv'.format(symbol,perM), index_col=0)
    if pys == 'FUTURE':
        btc_df = pd.read_csv('{}-{}-{}-data.csv'.format(symbol,'FUTURE',perM), index_col=0)
    if pys == 'FUTURE-SIM':
        btc_df = pd.read_csv('{}-{}-{}-data.csv'.format(symbol,'FUTURE',perM), index_col=0)
    
    src = btc_df['close']
    src2 = btc_df['close'].iloc[:-1]
    smrng = smoothrng(src, per, mult)
    filt_1 = rangefilter(src2, smrng)
    filt_2 = rangefilter(src, smrng)
    
    upward = 0.0
    downward = 0.0

    if (filt_2 > filt_1):
        upward = nz(upward) + 1
    if (filt_2 < filt_1):
        upward = 0
    else:
        upward = nz(upward)


    if (filt_2 < filt_1):
        downward = nz(downward) + 1
    if (filt_2 > filt_1):
        downward = 0
    else:
        downward = nz(downward)      
    
    
    #break outs
    longCond = False
    shortCond = False
    
    if ((src.iloc[-1] > filt_2) and (src.iloc[-1] > src.iloc[-2]) and (upward > 0)) or ((src.iloc[-1] > filt_2) and (src.iloc[-1] < src.iloc[-2]) and (upward > 0)): 
        longCond = True 
    
    if ((src.iloc[-1] < filt_2) and (src.iloc[-1] < src.iloc[-2]) and (downward > 0)) or ((src.iloc[-1] < filt_2) and (src.iloc[-1] > src.iloc[-2]) and (downward > 0)): 
        shortCond = True 
    
    CondIni = 0

    if longCond == True:
        CondIni = 1
    if longCond == False:
        if shortCond == True:
            CondIni = -1
    if pys == 'SPOT' or pys == 'MARGIN':
        fileHandle = open ( './{}signals{}.txt'.format(symbol,perM),"r" )
        lineList = fileHandle.readlines()
        fileHandle.close()
        
        try:
            prev_val = lineList[-1]
        except:
            prev_val = 'NON'

        f1=open('./{}signals{}.txt'.format(symbol,perM), 'a')
        signaling = 0
        
        if longCond == True and CondIni == 1:
            signaling = "AL"
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

                f1.close()
                return signaling
        
        if shortCond == True and CondIni == -1:
            signaling = "SAT"
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

                f1.close()
                return signaling
        f1.close()
        
        os.remove('{}-{}-data.csv'.format(symbol,perM))
    if pys == 'FUTURE':
        filename = ('./{}-{}-signals{}.txt'.format(symbol,pys,perM))
        file_exists = os.path.isfile(filename) 
        
        if file_exists:
            file = open(filename,"a+" )
            file.close()
        else:
            fileHandle = open ( './{}-{}-signals{}.txt'.format(symbol,pys,perM),"a" )
            fileHandle.close()
        fileHandle = open ( './{}-{}-signals{}.txt'.format(symbol,pys,perM),"r" )
        lineList = fileHandle.readlines()
        fileHandle.close()
        try:
            prev_val = lineList[-1]
        except:
            prev_val = 'NON'

        f1=open('./{}-{}-signals{}.txt'.format(symbol,pys,perM), 'a')
        signaling = 0
        
        if longCond == True and CondIni == 1:
            signaling = "AL"
            """
            if (signaling == prev_val):
                signaling = 0
            else:"""
            f1.write("\n")
            f1.write(signaling)

            f1.close()
            return signaling

        
        if shortCond == True and CondIni == -1:
            signaling = "SAT"
            """
            if (signaling == prev_val):
                signaling = 0
            else:"""
            f1.write("\n")
            f1.write(signaling)

            f1.close()
            return signaling

        else:
            """
            f1.write("\n")
            f1.write('non')
            f1.close()
            """
            return 'non'

        f1.close()
        
        #os.remove('{}-FUTURE-{}-data.csv'.format(symbol,perM))
    if pys == 'FUTURE-SIM':
        filename = ('./{}-FUTURE-signals{}.txt'.format(symbol,perM))
        file_exists = os.path.isfile(filename) 
        
        if file_exists:
            file = open(filename,"a+" )
            file.close()
        else:
            fileHandle = open ( './{}-FUTURE-signals{}.txt'.format(symbol,perM),"a" )
            fileHandle.close()

        fileHandle = open ( './{}-FUTURE-signals{}.txt'.format(symbol,perM),"r" )
        lineList = fileHandle.readlines()
        fileHandle.close()
        try:
            prev_val = lineList[-1]
        except:
            prev_val = 'NON'
        f1=open('./{}-FUTURE-signals{}.txt'.format(symbol,perM), 'a')
        signaling = 0
        
        if longCond == True and CondIni == 1:
            signaling = "AL"
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

                f1.close()
                
                return signaling
        
        if shortCond == True and CondIni == -1:
            signaling = "SAT"
            if (signaling == prev_val):
                signaling = 0
            else:
                f1.write("\n")
                f1.write(signaling)

                f1.close()
                
                return signaling
        f1.close()
        
        os.remove('{}-FUTURE-{}-data.csv'.format(symbol,perM))
    return 

def connect():
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False


def binance_rsi(symbol='ATOMUSDT',period=14,start_time="10 Jan, 2021",end_time="31 Jan, 2021"):
    get_all_binance(symbol, '5m', save = True)
    btc_df = pd.read_csv('{}-FUTURE-5m-data.csv'.format(symbol), index_col=0)
    return btalib.rsi(btc_df,period =14).df.rsi[-1],btalib.rsi(btc_df,period =14).df.rsi[-2]

def sim_profit():
    file ='kar.txt'
    f=open(file,"r")
    lines=f.readlines()
    result=[]
    for x in lines:
        result.append(x.split(' ')[-1][:5])
    f.close()

    if '\n' in result: 
        result.remove('\n')

    if any(item in result for item in '\n'):
        result[:2]

    list_of_floats = []
    for item in result:
        list_of_floats.append(float(item))
    print("Total profit=",sum(list_of_floats))
    return 

def futures_reactor_strategy(sembol,chart='1h',per1=8,per2=13,per3=21):
    def ema_builtin(symbol,perM,per):
        get_all_binance(symbol, perM, save = True,pysn='FUTURE')
        btc_df = pd.read_csv('{}-FUTURE-{}-data.csv'.format(symbol,perM), index_col=0)
        src = btc_df['close']
        return ta.trend.ema_indicator(src, per)

    low = ema_builtin(sembol, chart, per1)
    mid = ema_builtin(sembol, chart, per2)
    #high = ema_builtin(sembol, chart, per3)
    #print("EMA(8)=",low.iloc[-1])
    #print("EMA(13)=",mid.iloc[-1])
    filename = ('./{}ReactorSignals{}.txt'.format(sembol,chart))
    file_exists = os.path.isfile(filename) 
    
    if file_exists:
        file = open(filename,"a+" )
        file.close()

    f1=open(filename, 'a')

    if (low.iloc[-1] > mid.iloc[-1]):
        signal = 'AL'
        f1.write("\n")
        f1.write(signal)
    if (low.iloc[-1] < mid.iloc[-1]):
        signal = 'SAT'
        f1.write("\n")
        f1.write(signal)
    if abs(low.iloc[-1] - mid.iloc[-1]) <= 0.3:
        signal = 'Nonn'
        f1.write("\n")
        f1.write(signal)
    else:
        signal = 'NoN'
    f1.close()
    

    fileHandle = open(filename,"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    signal = lineList[-1]
    #print("REACTOR SIGNAL--->",signal)
    return signal


def spot_reactor_strategy(sembol,chart='15m',per1=8,per2=13,per3=21):
    low = ema_f(sembol, chart, per1)
    mid = ema_f(sembol, chart, per2)
    #high = ema_f(sembol, chart, per3)

    d1 = (low.iloc[-1] - low.iloc[-2])
    d2 = (mid.iloc[-1] - mid.iloc[-2])

    if (d1 * d2) > 0:
        kesim = False

    if (d1 * d2) < 0:
        kesim = True

    if (low.iloc[-1] >= low.iloc[-2]) and (kesim == True):
        signal = 'AL'
    if (low.iloc[-1] <= low.iloc[-2]) and (kesim == True):
        signal = 'SAT'
    if abs(low - mid) <=2:
        signal = 'Nonn'
    else:
        signal = 'NoN'
    
    return signal


def tp_sl(en_pr,slip,pos,price):
    en_p = float(en_pr)
    if (pos > 0):
        stop = price - (price * slip)
        if (price > en_p):
            stop = price - (price * slip)
    if pos < 0:
        stop = en_p + (en_p * slip)
        if (price < en_p):
            stop = price + (price * slip)
    #print("CURRENT STOP PRICE SET @",stop)
    return stop

def vol_calculator(sembol='BTCUSDT',piyasa='FUTURE',perM='1m'):
    "her dk değişimi al her birini 15 e bölüp topla"
    get_all_binance(sembol, perM, save = True,pysn=piyasa)
    btc_df = pd.read_csv('{}-FUTURE-{}-data.csv'.format(sembol,perM), index_col=0)
    srcc = btc_df['close']
    src = srcc.diff()
    last_pc = []
    for i in range(1,4):
        last_pc.append(src.iloc[-1*i]/5)
    last_pc.append((current_data_receiver(sembol,piyasa)[5]-srcc.iloc[-1])/5)
    return "{0:.3f}".format(float(sum(last_pc)))

def primary_main(per_pos,piyasa,aset1,aset2,sembol,per,mult,slip,quantityusr_first,quantityusr_2nd):
    client = Client(client_id, secret_key)
    if piyasa == 'FUTURE' or piyasa =='FUTURE-SIM': 

        b = client.futures_position_information()
        for i in range(len(b)):
                    if b[i]['symbol'] == sembol:
                        n= float(b[i]['positionAmt'])
                        en_pr= float(b[i]['entryPrice'])
        """
        if abs(float(n)) > 0:
            quantityusr_first = abs(float(n)*2)
        """
        if piyasa == 'FUTURE-SIM':
            tt = open('./{}lastprice_sim.txt'.format(sembol),"a+" )
            tt.close()
            tts = open('./{}pos.txt'.format(sembol),"a+" )
            tts.close()
            fileHandle = open ( './{}lastprice_sim.txt'.format(sembol),"r" )
            localizer = fileHandle.readlines()
            fileHandle.close()
            try:
                en_pr = localizer[-1]
            except:
                en_pr = 0
            s = open ( './{}pos.txt'.format(sembol),"r" )
            localizer = s.readlines()
            s.close()
            try:
                n = int(localizer[-1])
            except:
                n = 0
        if piyasa == 'FUTURE':

            rf = yess_rf_v2(sembol, '5m', 14, 0.8, 'FUTURE') #localizer2[-1]
            yess_rf_v2(sembol, '1h', per, mult, piyasa) #1saatlik range değeri almak için var
            
            fileHandle = open ( './{}-{}-signals15m.txt'.format(sembol,'FUTURE'),"r" )
            localizer = fileHandle.readlines()
            fileHandle.close()
            rfh = localizer[-1]

            frs = futures_reactor_strategy(sembol,'5m',8,13,21)
            inf = current_data_receiver(sembol,'FUTURE')
            price = inf[5]
            btc_df = pd.read_csv('{}-FUTURE-{}-data.csv'.format(sembol,'5m'), index_col=0)
            high = "{0:.3f}".format(float(btc_df['high'].iloc[-1]))
            low = "{0:.3f}".format(float(btc_df['low'].iloc[-1]))
            """
            fh = open ( './{}ReactorSignals15m.txt'.format(sembol),"r" )
            lc = fh.readlines()
            fh.close()
            lastsaved = lc[-1]
            
            if lc[-1] != lc[-2]:
                frs = lastsaved        
            """
            return rf, rfh, frs, price, quantityusr_first, quantityusr_2nd,n,en_pr,high,low
    if piyasa == 'SPOT':
        #bu kısım future hesabına göre düzenlenmeli
        quantityusr_2nd = "{0:.3f}".format(float(client.futures_account_balance(asset=aset1)['free'])*per_pos)
        quantityusr_first = "{0:.3f}".format(float(client.futures_account_balance(asset=aset2)['free'])/float(current_data_receiver(sembol)[5])*per_pos)
    if piyasa == 'MARGIN':
        #bu kısım future hesabına göre düzenlenmeli
        quantityusr_2nd = "{0:.3f}".format(float(client.get_asset_balance(asset=aset1)['free'])*per_pos)
        quantityusr_first = "{0:.3f}".format(float(client.get_asset_balance(asset=aset2)['free'])/float(current_data_receiver(sembol)[5])*per_pos)
    if piyasa == "SPOT" or piyasa == "MARGIN":
        quantityusr_2nd = "{0:.3f}".format(float(client.get_asset_balance(asset=aset1)['free'])*per_pos)
        quantityusr_first = "{0:.3f}".format(float(client.get_asset_balance(asset=aset2)['free'])/float(current_data_receiver(sembol)[5])*per_pos)
    return 

def secondary_main(sembol,piyasa,per_pos,quantityusr_first,quantityusr_2nd):
    client = Client(client_id, secret_key)
    inf = current_data_receiver(sembol,piyasa)
    price = inf[5]
    btc_df = pd.read_csv('{}-FUTURE-{}-data.csv'.format(sembol,'5m'), index_col=0)
    high = btc_df['high'].iloc[-1]
    low = btc_df['low'].iloc[-1]
    
    b = client.futures_position_information()
    for i in range(len(b)):
                if b[i]['symbol'] == sembol:
                    n= float(b[i]['positionAmt'])
                    en_pr= float(b[i]['entryPrice'])
    #profit = ((float(price)-float(en_pr)) / float(en_pr))
    if abs(float(n)) > 0:
        quantityusr_first = abs(float(n)*2)
    
    if piyasa == 'FUTURE-SIM':
        tt = open('./{}lastprice_sim.txt'.format(sembol),"a+" )
        tt.close()
        tts = open('./{}pos.txt'.format(sembol),"a+" )
        tts.close()
        fileHandle = open ( './{}lastprice_sim.txt'.format(sembol),"r" )
        localizer = fileHandle.readlines()
        fileHandle.close()
        try:
            en_pr = localizer[-1]
        except:
            en_pr = 0

        s = open ( './{}pos.txt'.format(sembol),"r" )
        localizer = s.readlines()
        s.close()
        try:
            n = int(localizer[-1])
        except:
            n = 0

    #print("IN POSITION PRICE",en_pr)
    rf5 = yess_rf_v2(sembol, '5m', 14, 0.8, piyasa) #localizer2[-1]
    
    fileHandle = open ( './{}-FUTURE-signals15m.txt'.format(sembol),"r" )
    localizer = fileHandle.readlines()
    fileHandle.close()
    rfh = localizer[-1]

    fh = open ( './{}-FUTURE-signals5m.txt'.format(sembol),"r" )
    lc = fh.readlines()
    fh.close()
    lastsaved = lc[-1]
    
    if localizer[-1] != localizer[-2]:
        rf5 = lastsaved


    frs = futures_reactor_strategy(sembol,'5m',8,13,21)
    #print("RANGE FILTER CURRENT SIGNAL @ 5m PERIOD IS-->",rf5)
    #print("RANGE FILTER CURRENT SIGNAL @ 15m PERIOD IS-->",rfh)
    return frs, rfh, quantityusr_2nd, quantityusr_first, rf5, 'NON', en_pr, price,n,low,high
def multip_b(price,multiplier):
    n = "{}".format(price)
    basamak = n[::-1].find('.')
    return round((float(price)*multiplier),basamak)

def strategy_inlet(frs,key,rfh,n,price,sembol, piyasa,order_type,quantityusr_first,keyn,strategy,rf,slip,en_pr,high,low):
    #rf5 = yess_rf_v2(sembol, '5m', 14, 0.8, 'FUTURE')
    op = 'NON'
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "range_5":
        if rf5 == 'AL':
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            if keyn == "on":
                key = True
                op = "AL"          
            print("ALIŞ")
        if rf5 == 'SAT':
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            if keyn == "on":
                key = True
                op = "SAT"  
            print("SATIŞ")    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "range":
        stop_price = tp_sl(en_pr,slip,n,price)
        if ((frs == "AL") and (key == False) and (rfh == "AL") and (n <= 0)) or (price <= stop_price and strategy == "range"):
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)  
            if keyn == "on":
                key = True
                op = "AL"          
            print("ALIŞ")
        if ((rf == "SAT" ) and (key == False) and (n >= 0))or (price >= stop_price and strategy == "range"):
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            if keyn == "on":
                key = True
                op = "SAT"  
            print("SATIŞ")
        if (frs == 'SAT' and n < 0) or (frs == 'AL' and n > 0 and strategy == "range"):
            key = True
            if n < 0:
                op = 'SAT'
            else:
                op = 'AL'
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    #print(rf5,frs)
    if strategy == "range_ema_stopless":
        if ((frs == "AL") and  (key == False) and (frs == "AL") and (n <= 0)):
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)  
            key = True
            op = "AL"          
            print("ALIŞ @ {}".format(price))
        if ((rf5 == "SAT") and (key == False) and (frs == "SAT") and (n >= 0)):
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            key = True
            op = "SAT"  
            print("SATIŞ @ {}".format(price))
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "range_tp":
        rf5 = yess_rf_v2(sembol, '5m', 14, 1, 'FUTURE')
        slip = 0.002
        vl = vol_calculator(sembol,'FUTURE','3m')
        
        print("RANGE SİNYAL=",rf5,"ANLIK FİYAT=",price,"Pozisyon Büyüklüğü:",n,"HACİM=",vl,"EMA",frs,"SEMBOL",sembol)
        if n == 0:
            client.futures_cancel_all_open_orders(symbol=sembol)

        if ((rf5 == "SAT" and strategy == "range_tp") and (key == False) and (n == 0)):
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key) 
            
            b = client.futures_position_information()
            for i in range(len(b)):
                if b[i]['symbol'] == sembol:
                    en_pr= float(b[i]['entryPrice'])
            print("ENTRY PRICE:",en_pr)
            stop_price = float("{0:.2f}".format(en_pr - (en_pr * slip/2)))

            tp = float("{0:.2f}".format(en_pr + (en_pr * slip)))
            #client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
            #client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_TAKE_PROFIT_MARKET, stopPrice=tp,quantity=quantityusr_first) 
            key = True
            op = "AL"          
            print("ALIŞ @ {}".format(price))
        if ((rf5 == "AL" and strategy == "range_tp") and (key == False) and (n == 0)):
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
    
            b = client.futures_position_information()
            for i in range(len(b)):
                if b[i]['symbol'] == sembol:
                    en_pr= float(b[i]['entryPrice'])
            print("ENTRY PRICE:",en_pr)

            stop_price = float("{0:.2f}".format(en_pr + (en_pr * slip/2)))
            tp = float("{0:.2f}".format(en_pr - (en_pr * slip)))
            #client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
            #client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_TAKE_PROFIT_MARKET, stopPrice=tp,quantity=quantityusr_first) 
            key = True
            op = "SAT"  
            print("SATIŞ @ {}".format(price))
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "terminator":
        if (rf5 == "AL" and key == False and n == 0):
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key) 
            key = True
            op = "AL"          
            print("ALIŞ @ {}".format(price))
        if (rf5 == "SAT" and key == False and n == 0):
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            key = True
            op = "SAT"  
            print("SATIŞ @ {}".format(price))        
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "supernova":
        vl = float(vol_calculator(sembol=sembol,piyasa='FUTURE',perM='1m'))
        c=client.futures_get_open_orders(symbol=sembol)
        low = float(low)
        high = float(high)
        for i in range(len(c)):
            try: 
                if c[i]['type'] == 'STOP_MARKET':
                    order = c[i]['orderId']
                    stopPrice = c[i]['stopPrice']
                else:
                    print("error")
            except:
                print("error")
        #print(rf5,frs,low,high)
        if n > 0:
            #stop_price = float("{0:.2f}".format(en_pr - (en_pr * slip)))
            try:
                if price > (en_pr+1):
                    stop_price = price-1
                    if stop_price > float(stopPrice) and ((high - low) < 3):
                        print("+NEW STOP PRICE SET @",stop_price)
                        client.futures_cancel_order(symbol=sembol, orderId=order)
                        client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
                    if (((high - low) > 3) and (price > (high-((high - low)*0.4))) and (low > en_pr)):
                        stop_price = "{0:.2f}".format(float((low+((high-low)*0.20))))
                        print("+NEW STOP PRICE SET @",stop_price)
                        client.futures_cancel_order(symbol=sembol, orderId=order)
                        client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
                    else:
                        print("+NEW STOP PRICE NOT SET ")
            except:
                print("ERROR OCC. @ SPNV - ST - IN")
            if (price < high):
                if (price < en_pr+1) and (price > (high-((high - en_pr)*0.5)) and (abs(vl)>1)):
                    stop_price = "{0:.2f}".format(float((en_pr+((high-en_pr)*0.30))))
                    client.futures_cancel_order(symbol=sembol, orderId=order)
                    client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
                else:
                    print("+NEW STOP PRICE NOT SET +++")
            else:
                print("+NEW STOP PRICE NOT SET ")
            
        if n < 0:
            #stop_price = float("{0:.2f}".format(en_pr - (en_pr * slip)))
            if price < (en_pr-1):
                stop_price = price+1
                if stop_price < float(stopPrice) and ((high - low) < 3):
                    print("-NEW STOP PRICE SET @",stop_price)
                    client.futures_cancel_order(symbol=sembol, orderId=order)
                    client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
                if (((high - low) > 3) and (price < (low+((high - low)*0.4))) and (high < en_pr)):
                    stop_price = "{0:.2f}".format(float((high+((high-low)*0.20))))
                    print("-NEW STOP PRICE SET @",stop_price)
                
                else:
                    print("-NEW STOP PRICE NOT SET ")
            
            if (price > low):
                if (price > en_pr-1) and (price < (low+((en_pr-low)*0.5)) and (abs(vl)>1)):
                    stop_price = "{0:.2f}".format(float((en_pr-((en_pr-low)*0.30))))
                    client.futures_cancel_order(symbol=sembol, orderId=order)
                    client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
                else:
                    print("-NEW STOP PRICE NOT SET ")
            else:
                print("-NEW STOP PRICE NOT SET ")
            
            
        #print("CURRENT SIGNAL",rf5)
        
        #rf5 = yess_rf_v2(sembol, '5m', 14, 0.8, piyasa)
        s1=open('./kar.txt', 'a')
        if ((rf5 == "AL") and (frs == "AL") and (key == False) and (n == 0)):
            stop_price = price-1
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)  
            s1.write("\n")
            try:
                print(sembol,"ENTRY PRICE:",en_pr,"CURRENT PRICE",price,"STOP PRICE",stop_price,"RF",rf,"KAR %",((price-en_pr)/en_pr)*100)
                s1.write('{} ALIŞ @ {} KAR % {}'.format(sembol,price,(((price-en_pr)/en_pr)*100)))
            except:
                print(sembol,"ENTRY PRICE:",en_pr,"CURRENT PRICE",price,"STOP PRICE",stop_price,"RF",rf)
                s1.write('{} ALIŞ @ {} KAR % 0'.format(sembol,price))
            key = True
            op = "AL"          
            
            
            client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
        
        if ((rf5 == "SAT" ) and (frs == "SAT") and (key == False) and (n == 0)):
            stop_price = price+1
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            s1.write("\n")
            try:
                print(sembol,"ENTRY PRICE:",en_pr,"CURRENT PRICE",price,"STOP PRICE",stop_price,"RF",rf,"KAR %",((en_pr-price)/en_pr)*100)
                s1.write('{} SATIŞ @ {} KAR % {}'.format(sembol,price,(((en_pr-price)/en_pr)*100)))
            except:
                print(sembol,"ENTRY PRICE:",en_pr,"CURRENT PRICE",price,"STOP PRICE",stop_price,"RF",rf)
                s1.write('{} SATIŞ @ {} KAR % 0'.format(sembol,price))
            key = True
            op = "SAT"  
            
            
            client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
        
        else:
            0 == 0
        s1.close()
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "japoncu1":
        sgnl = yess_rf_heinekenashi(sembol, '5m', 100, 0.8,pys='FUTURE')
        if (sgnl == "AL" and key == False):
            if n == 0:
                buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key) 
                tp = "{0:.2f}".format(float(price)*1.005)
                client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_TAKE_PROFIT_MARKET, stopPrice=tp,quantity=quantityusr_first) 
            else:
                print("ERROR OCC @ BUY",sembol)
            key = True
            op = "AL"          
            #print("ALIŞ @ {}".format(price))
        if (sgnl == "SAT" and key == False):
            if n == 0:
                sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
                tp = "{0:.2f}".format(float(price)*0.995)
                client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_TAKE_PROFIT_MARKET, stopPrice=tp,quantity=quantityusr_first) 
            else:
                print("ERROR OCC @ SELL",sembol)
            key = True
            op = "SAT"  
            #print("SATIŞ @ {}".format(price))   
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "japoncu":
        if n == 0:
            print("running")
            #client.futures_cancel_all_open_orders(symbol=sembol)
            sgnl = yess_rf_heinekenashi(sembol, '1h', 100, 0.1,pys='FUTURE')
            print(vol_calculator(sembol,'FUTURE','1h'))
            if (sgnl == "AL" and key == False):
                buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key) 
                tp = "{0:.2f}".format(float(price)*1.01)
                stop_price = "{0:.2f}".format(float(price)*0.995)
                client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_TAKE_PROFIT_MARKET, stopPrice=tp,quantity=quantityusr_first)
                client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first) 
                key = True
                op = "AL"        
                time.sleep(20)  
            if (sgnl == "SAT" and key == False):
                sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
                tp = "{0:.2f}".format(float(price)*0.99)
                stop_price = "{0:.2f}".format(float(price)*1.005)
                client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_TAKE_PROFIT_MARKET, stopPrice=tp,quantity=quantityusr_first) 
                client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type=client.ORDER_TYPE_STOP_MARKET, stopPrice=stop_price,quantity=quantityusr_first)
                key = True
                op = "SAT"  
                time.sleep(20)
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "packman":
        if n == 0:
            if len(client.futures_get_open_orders(symbol=sembol)) > 0:
                client.futures_cancel_all_open_orders(symbol=sembol)
                print("Open orders canceled")
            f = binance_rsi(sembol,period =14,start_time="10 Apr, 2021",end_time="27 Apr, 2021")
            rsi = f[0]
            rsi_prev = f[1]
            if (rsi > 60 and rsi < 70) or (rsi < 40 and rsi > 30):
                print("rsi:",rsi,"rsi previous candle:",rsi_prev,sembol)
            
            if (rsi <=30 and key == False and rsi_prev <= rsi):
                print("BUY ORDER SENDING  @",price)
                #buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key) 
                tp = multip_b(price,1.005)
                stop_price = multip_b(price,0.995)
                print("BUY ORDER SENDED...")
                """
                try:
                    client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="TAKE_PROFIT_MARKET", stopPrice=tp,quantity=quantityusr_first)
                except:
                    client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="TAKE_PROFIT_MARKET", stopPrice=tp,quantity=quantityusr_first)
                try:
                    client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first) 
                except:
                    client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first) 
                """
                print("BUY ORDER TP&SL SET!...","TP:",tp,"SL:",stop_price)
                key = True
                op = "AL"        
                time.sleep(10)  

            if (rsi >= 70 and key == False and rsi_prev >= rsi):
                print("SELL ORDER SENDING  @",price)
                #sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
                print("SELL ORDER SENDED...")
                tp = multip_b(price,1.005)
                stop_price = multip_b(price,0.995)
                """
                try:
                    client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="TAKE_PROFIT_MARKET", stopPrice=tp,quantity=quantityusr_first) 
                except:
                    client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="TAKE_PROFIT_MARKET", stopPrice=tp,quantity=quantityusr_first) 
                
                try:
                    client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first)
                except:
                    client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first)
                """
                print("SELL ORDER TP&SL SET!...","TP:",tp,"SL:",stop_price)
                key = True
                op = "SAT"  
                time.sleep(10)
            
            if (rsi < 65 and rsi > 35 and key == False and 1 == 1):
                dos = 0.8
                sgnl = yess_rf_heinekenashi(sembol, '5m', 100, 0.4,pys='FUTURE')
                print("range module ACTIVE+","Volume Calc:",vol_calculator(sembol,'FUTURE','5m'),"Current Signal:",sgnl,sembol)
                if (sgnl == "AL" and key == False):
                    #buy_module(sembol, piyasa,order_type,multip_b(quantityusr_first,dos),price,keyn,client_id, secret_key) 
                    tp = multip_b(price,1.005)
                    stop_price = multip_b(price,0.995)
                    """
                    try:
                        client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="TAKE_PROFIT_MARKET", stopPrice=tp,quantity= multip_b(quantityusr_first,dos))
                    except:
                        client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="TAKE_PROFIT_MARKET", stopPrice=tp,quantity= multip_b(quantityusr_first,dos))
                    try:
                        client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="STOP_MARKET", stopPrice=stop_price,quantity= multip_b(quantityusr_first,dos)) 
                    except:
                        client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="STOP_MARKET", stopPrice=stop_price,quantity= multip_b(quantityusr_first,dos)) 
                    """
                    print("BUY ORDER TP&SL SET!...","TP:",tp,"SL:",stop_price)
                    key = True
                    op = "AL"        
                    time.sleep(5)  
                    print("ALIŞ @",price)
                if (sgnl == "SAT" and key == False):
                    #sell_module(sembol, piyasa,order_type,multip_b(quantityusr_first,dos),price,keyn,client_id, secret_key)
                    tp = multip_b(price,0.995)
                    stop_price = multip_b(price,1.005)
                    """
                    try:
                        client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="TAKE_PROFIT_MARKET", stopPrice=tp,quantity= multip_b(quantityusr_first,dos)) 
                    except:
                        client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="TAKE_PROFIT_MARKET", stopPrice=tp,quantity= multip_b(quantityusr_first,dos)) 
                    
                    try:
                        client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="STOP_MARKET", stopPrice=stop_price,quantity= multip_b(quantityusr_first,dos))
                    except:
                        client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="STOP_MARKET", stopPrice=stop_price,quantity= multip_b(quantityusr_first,dos))
                    """
                    print("SELL ORDER TP&SL SET!...","TP:",tp,"SL:",stop_price)
                    key = True
                    op = "SAT"  
                    time.sleep(5)
                    print("SATIŞ @",price)            
        """
        if n != 0:
            c=client.futures_get_open_orders(symbol=sembol)
            low = float(low)
            high = float(high)
            for i in range(len(c)):
                try: 
                    if c[i]['type'] == 'STOP_MARKET':
                        order = c[i]['orderId']
                        stopPrice = c[i]['stopPrice']
                    else:
                        print("error")
                except:
                    print("error")
            if n > 0:
                stop_price = float("{0:.2f}".format(en_pr - (en_pr * slip)))
                try:
                    if price > (en_pr+1):
                        stop_price = price-1
                        if stop_price > float(stopPrice) and ((high - low) < 3):
                            print("+NEW STOP PRICE SET @",stop_price)
                            client.futures_cancel_order(symbol=sembol, orderId=order)
                            client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first)
                        if (((high - low) > 3) and (price > (high-((high - low)*0.4))) and (low > en_pr)):
                            stop_price = "{0:.2f}".format(float((low+((high-low)*0.20))))
                            print("+NEW STOP PRICE SET @",stop_price)
                            client.futures_cancel_order(symbol=sembol, orderId=order)
                            client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first)
                        else:
                            print("+NEW STOP PRICE NOT SET ")
                except:
                    print("ERROR OCC. @ SPNV - ST - IN")
                if (price < high):
                    if (price < en_pr+1) and (price > (high-((high - en_pr)*0.5)) and (abs(vl)>1)):
                        stop_price = "{0:.2f}".format(float((en_pr+((high-en_pr)*0.30))))
                        client.futures_cancel_order(symbol=sembol, orderId=order)
                        client.futures_create_order(symbol=sembol,side=client.SIDE_SELL,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first)
                    else:
                        print("+NEW STOP PRICE NOT SET +++")
                else:
                    print("+NEW STOP PRICE NOT SET ")
                
            if n < 0:
                stop_price = float("{0:.2f}".format(en_pr - (en_pr * slip)))
                if price < (en_pr-1):
                    stop_price = price+1
                    if stop_price < float(stopPrice) and ((high - low) < 3):
                        print("-NEW STOP PRICE SET @",stop_price)
                        client.futures_cancel_order(symbol=sembol, orderId=order)
                        client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first)
                    if (((high - low) > 3) and (price < (low+((high - low)*0.4))) and (high < en_pr)):
                        stop_price = "{0:.2f}".format(float((high+((high-low)*0.20))))
                        print("-NEW STOP PRICE SET @",stop_price)
                    
                    else:
                        print("-NEW STOP PRICE NOT SET ")
                
                if (price > low):
                    if (price > en_pr-1) and (price < (low+((en_pr-low)*0.5)) and (abs(vl)>1)):
                        stop_price = "{0:.2f}".format(float((en_pr-((en_pr-low)*0.30))))
                        client.futures_cancel_order(symbol=sembol, orderId=order)
                        client.futures_create_order(symbol=sembol,side=client.SIDE_BUY,type="STOP_MARKET", stopPrice=stop_price,quantity=quantityusr_first)
                    else:
                        print("-NEW STOP PRICE NOT SET ")
                else:
                    print("-NEW STOP PRICE NOT SET ")"""
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------  
    else:
        key = False
        #print("NO OPERATION")
    return op, key

def strategy_outlet(op, rf5, strategy,n,price,sembol, piyasa,order_type,quantityusr_first,profit,keyn,en_pr,slip,frs):
    #stop_price = tp_sl(en_pr,slip,n,price)
    k = True
    r = True
    #print("--",op,"RF 5min",rf5, "POS",n,"price",price,"STOP@",stop_price)
    op = 'NON'
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "range_5":
        if rf5 == 'AL' and strategy == "range_5":
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            if keyn == "on":
                key = True
                op = "AL"          
            print("ALIŞ")
        if rf5 == 'SAT'and strategy == "range_5":
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            if keyn == "on":
                key = True
                op = "SAT"  
            print("SATIŞ")    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "range":
        if (op == "AL" and (rf5 == "SAT") and (strategy == "range") and (float(n) > 0 or float(n) == 0)) or ((float(n) > 0 or float(n) == 0) and (price <= stop_price)): 
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            print("SATIŞ")
            op = 'SAT'
            k = False
            r = False
        if ((frs == "AL") and (strategy == "range") and (float(n) < 0 or float(n) == 0)) or ((float(n) < 0 or float(n) == 0) and (price >= stop_price)): 
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            print("ALIŞ")
            op = 'AL'
            k = False
            r = False
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy == "range_ema_stopless":
        if ((rf5 == "SAT") and (strategy == "range_ema_stopless") and (float(n) > 0 or float(n) == 0)): 
            sell_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            print("SATIŞ @ {}".format(price))
            op = 'SAT'
            k = False
            r = False
        if ((rf5 == "AL") and (strategy == "range_ema_stopless") and (float(n) < 0 or float(n) == 0)): 
            buy_module(sembol, piyasa,order_type,quantityusr_first,price,keyn,client_id, secret_key)
            print("ALIŞ @ {}".format(price))
            op = 'AL'
            k = False
            r = False
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    if strategy=='range_tp' or strategy == "supernova" or strategy == "japoncu" or strategy=="packman":
        op = 'SAT'
        k = False
        r = False 
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    else:
        op = 'NON'
    return op, k, r