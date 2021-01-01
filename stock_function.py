from twstock import Stock, codes, realtime
from datetime import datetime
from estimate_capacity_weight import weight
import math

def close_price(stock_num):
    stock = Stock(stock_num)
    return stock.price

def capacity(stock_num):
    stock = Stock(stock_num)
    return math.floor(stock.capacity[-1]/1000)

def name(stock_num):
    return codes[stock_num].name

def real_time(stock_num):
    stock = realtime.get(stock_num)
    return stock

def accu_capacity(stock_num):
    real_time_stock = real_time(stock_num)
    if real_time_stock['success']:
        accu_capacity = real_time_stock['realtime']['accumulate_trade_volume']
        return accu_capacity
    else:
        return 0

def accu_capacity_multi(stock_nums):
    real_time_stocks = realtime.get(stock_nums)
    accu_capacitys = [real_time_stocks[stock_num]['realtime']['accumulate_trade_volume'] for stock_num in stock_nums]
    return accu_capacitys

def estimated_capacity(ac):
    now = datetime.now().strftime("%H:%M")
    now = list(now)
    print(now)
    now[-1] = str(int((int(now[-1]) // 5) * 5))
    now = ''.join(now)
    print(now)

    if now in weight:
        return math.floor(int(ac) * weight[now])
    else:
        return '-'
