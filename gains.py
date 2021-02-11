import cbpro
import json
import sys

# How to use:
#
# python gains.py <currency> <credentials file>
#
#   currency is e.g. BTC-USD for Bitcoin.
#   credentials file should be JSON in this form:
#   {
#       "key": "",
#       "passphrase": "",
#       "secret" : ""
#   }

# Step 0: args
currency = sys.argv[1]
cred_file = sys.argv[2]

# Step 1: auth with Coinbase
with open(cred_file) as f:
    creds = json.load(f)

private_client = cbpro.AuthenticatedClient(creds['key'], creds['secret'], creds['passphrase'])

# Step 2: Get the fills for the chosen currency
fills_generator = private_client.get_fills(currency)

# Step 3: Gather the information we need to calculate profit/loss
usd_spent = 0
coins_accumulated = 0
for fill in fills_generator:
    usd_spent += float(fill['usd_volume'])
    coins_accumulated += float(fill['size']) # TODO: check if sells are negative
    pass

# Step 4: Get the current price of our currency
price = float(private_client.get_product_ticker(currency)['price'])

# Step 5: Do our calculations
cost_basis = (usd_spent / coins_accumulated)
profit_loss = ((price / cost_basis) - 1.0) * 100.0

# Step 6: Print it out nicely!
print("You spent ${:.2f} USD to buy {} {}".format(usd_spent, coins_accumulated, currency))
print("Your cost basis is ${:.2f} per {}".format(cost_basis, currency))
print("The current price is ${:.2f}, leaving you with a return of {:.2f}%".format(price, profit_loss))