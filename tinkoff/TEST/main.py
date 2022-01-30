# pip install python_dateutil


# from openapi_client import openapi
from lib.openapi import sandbox_api_client
from lib.api.market_api import MarketApi
from datetime import datetime, timedelta
# from pytz import timezone

token = 't.ySIWEI9WCjLvyZhsq3h__dNhf7r1A6KOWK6cfR1N07Z9BSFZKcHM6UC1NgR4MIUR3Pq_eQhhqiEyvgWq8JXCvQ'
client = sandbox_api_client(token)

market = MarketApi(client)
# print(client)
bnd = market.market_bonds_get()
print(bnd)



