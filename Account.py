import csv
from Stock import Stock

class Account:
    def __init__(self):
        self.stocks = {}

        with open("rh.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if(row['state'] == 'filled'):
                    self.put_in_stocks(row)

        def sort_stocks(stock):
            chain = stock.chain
            chain.sort(key=lambda x: x['price'], reverse=False)

        def reduce_chain(stock):
            def reduce_forwards(buy_chain, transaction):
                profit = 0.0
                total_sold = transaction['cumulative_quantity']
                #print('selling ' + str(total_sold))
                for buy_transaction in buy_chain:
                    if(total_sold == 0.0):
                        break
                    if(buy_transaction['cumulative_quantity'] > 0.0):
                        difference = total_sold - buy_transaction['cumulative_quantity']
                        if(difference == 0.0):
                            profit += total_sold * (transaction['price'] - buy_transaction['price'])
                            #print('reducing from ' + str(buy_transaction['cumulative_quantity']) + " to " + str(0))
                            buy_transaction['cumulative_quantity'] = 0.0
                            total_sold = 0.0
                        elif(difference >= 1.0):
                            profit += buy_transaction['cumulative_quantity'] * (transaction['price'] - buy_transaction['price'])
                            #print('reducing from ' + str(buy_transaction['cumulative_quantity']) + " to " + str(0))
                            total_sold -= buy_transaction['cumulative_quantity']
                            buy_transaction['cumulative_quantity'] = 0.0
                        elif(difference <= -1.0):
                            profit += total_sold * (transaction['price'] - buy_transaction['price'])
                            #print('reducing from ' + str(buy_transaction['cumulative_quantity'])  + " to " + str(buy_transaction['cumulative_quantity'] - total_sold))
                            buy_transaction['cumulative_quantity'] -= total_sold
                            total_sold = 0.0
                        else:
                            raise
                transaction['profit'] = profit
                        
                        

            def group_chain(chain):
                buy_chain = []
                sell_chain = []

                for transaction in chain:
                    if(transaction['side'] == 'buy'):
                        buy_chain.append(transaction)
                    else:
                        sell_chain.append(transaction)
                return buy_chain, sell_chain

            chain = stock.chain
            (buy_chain, sell_chain) = group_chain(chain)
            for transaction in sell_chain:
                reduce_forwards(buy_chain, transaction)
            stock.chain = buy_chain + sell_chain

        def update_price_avg(stock):
            total = 0.0
            total_shares = 0
            for transaction in stock.chain:
                if(transaction['side'] == 'buy' and transaction['cumulative_quantity'] >= 1):
                    #if(transaction['symbol'] == 'MU'):
                        #print transaction['cumulative_quantity']
                        #print transaction['price']
                    total_shares += transaction['cumulative_quantity']
                    total += transaction['cumulative_quantity'] * transaction['price']
            #if(stock.symbol == 'MU'):
                #print(total)
                #print(total_shares)
            stock.num_shares = total_shares
            try:
                stock.avg_price = total / stock.num_shares
            except:
                stock.avg_price = 0
        
        def set_realized_gains(stock):
            total = 0
            for transaction in stock.chain:
                if(transaction['side'] == 'sell'):
                    total += transaction['profit']
            stock.realized_gains = total

            
        self.map_stocks(sort_stocks)
        self.map_stocks(reduce_chain)
        self.map_stocks(update_price_avg)
        self.map_stocks(set_realized_gains)
        
    def put_in_stocks(self, row):
        if(not self.stocks.has_key(row['symbol'])):
            self.stocks[row['symbol']] = Stock(row['symbol'])
        stock = self.stocks[row['symbol']]
        stock.add(row)

    def map_stocks(self,function):
        for symbol in self.stocks:
            stock = self.stocks[symbol]
            function(stock) 

    def current_positions(self):
        def print_positions(stock):
            print stock.symbol
            print stock.num_shares
            print stock.avg_price
        self.map_stocks(print_positions)
    
    def stock_chain(self):
        def print_chain(stock):
            print stock.chain
        self.map_stocks(print_chain)
