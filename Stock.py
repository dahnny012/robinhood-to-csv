class Stock:
    def __init__(self, symbol):
        self.num_shares = 0
        self.avg_price = 0
        self.symbol = symbol
        self.chain = []
        self.realized_gains = 0

    
    def add(self, row):
        self.chain_add(row)
        self.update(row)

    def chain_add(self, row):
        new_row = dict(row)
        new_row['cumulative_quantity'] = float(new_row['cumulative_quantity'])
        new_row['quantity'] = float(new_row['quantity'])
        new_row['price'] = float(new_row['price'])
        new_row['timestamp'] = new_row['timestamp']
        self.chain.append(new_row)

    def update(self, row):
        self.num_shares += self.add_or_reduce_stock(row)
        self.avg_price = self.calculate_average()

    def calculate_average(self):
        total = 0.0
        for stock in self.chain:
            if(stock['side'] == "buy"):
                total += float(stock['cumulative_quantity']) * float(stock['price'])
            else:
                total -= float(stock['quantity']) * float(stock['price'])

        if(self.num_shares == 0.0):
            return 0.0
        return total / self.num_shares

    def add_or_reduce_stock(self, row):
        if(row['side'] == "sell"):
            return -1 * float(row['cumulative_quantity'])
        else:
            return float(row['cumulative_quantity'])