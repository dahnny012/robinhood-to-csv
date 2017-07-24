from Account import Account
import os, json, csv
from googlefinance import getQuotes
from time import gmtime, strftime
import glob, csv, xlwt, os


account = Account()

path = "./stocks/" + strftime("[%Y-%m-%d-%H-%M-%S]", gmtime()) + "/"

try: 
    os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise
keys = ['cumulative_quantity', 'price', 'side']
def print_chain_to_files(stock):
    with open(path + stock.symbol + ".csv", 'wb') as stock_file:
        current_price = float(getQuotes([stock.symbol])[0]['LastTradePrice'])
        gain = current_price * stock.num_shares - stock.num_shares * stock.avg_price 
        total_gains = current_price * stock.num_shares - stock.num_shares * stock.avg_price + stock.realized_gains
        try:
            percent_gain = 100 - (stock.avg_price * stock.num_shares) / (current_price * stock.num_shares) * 100
        except:
            percent_gain = 0
        stock_csv = csv.writer(stock_file)
        stock_csv.writerow(['symbol','total', 'avg_price', 'current_price', 'gain if sold', 'percent_gain', 'realized_gains', 'total gains'])
        stock_csv.writerow([stock.symbol, stock.num_shares, stock.avg_price, current_price, gain, percent_gain, stock.realized_gains, total_gains])
        stock_csv.writerow('')
        stock_csv.writerow(keys + ['gain/profit', 'percent_gain'])
        for transaction in stock.chain:
            row = []
            for key in keys:
                row.append(transaction[key])
            if(transaction['side'] == 'buy'):
                row.append(current_price * float(transaction['cumulative_quantity']) - float(transaction['price']) * float(transaction['cumulative_quantity']))
                row.append(100 - (float(transaction['price']) * 100.0 / current_price))
            if(transaction['side'] == 'sell'):
                row.append(float(transaction['profit']))
            stock_csv.writerow(row)


def merge_csv_into_xls():
    wb = xlwt.Workbook()
    files = os.listdir(path)
    for filename in map(lambda x: path + x, files):
        f_name = filename.split(path)[1]
        f_short_name = f_name.split(".csv")[0]
        ws = wb.add_sheet(f_short_name)
        spamReader = csv.reader(open(filename, 'rb'))
        for rowx, row in enumerate(spamReader):
            for colx, value in enumerate(row):
                #lmao
                if(colx == 0 and rowx > 3):
                    ws.write(rowx, colx, float(value))
                elif(colx == 1 and rowx != 0 and rowx != 3):
                    ws.write(rowx, colx, float(value))
                elif(rowx == 1):
                    if(colx == 2 or colx == 3):
                        ws.write(rowx, colx, float(value))
                    else:
                        ws.write(rowx, colx, value)
                else:
                    ws.write(rowx, colx, value)
    wb.save(path+"portfolio.xls")

account.map_stocks(print_chain_to_files)
merge_csv_into_xls()
