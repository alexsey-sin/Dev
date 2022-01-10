from openapi_client import openapi
from datetime import datetime, timedelta
from pytz import timezone

token = 't.ySIWEI9WCjLvyZhsq3h__dNhf7r1A6KOWK6cfR1N07Z9BSFZKcHM6UC1NgR4MIUR3Pq_eQhhqiEyvgWq8JXCvQ'
client = openapi.sandbox_api_client(token)
# client.sandbox.sandbox_register_post()  # Регистрация клиента в sandbox
# client.sandbox.sandbox_clear_post()  # Удаление всех позиций  в sandbox

# Выставление баланса по валютным позициям в sandbox
# client.sandbox.sandbox_currencies_balance_post(sandbox_set_currency_balance_request={"currency": "USD", "balance": 1000})


def set_balance():
    balance_set = client.sandbox.sandbox_currencies_balance_post({"currency": "USD", "balance": 10000})
    print("balance")
    print(balance_set)
    print()


def print_24hr_operations():
    now = datetime.now(tz=timezone('Europe/Moscow'))
    yesterday = now - timedelta(days=1)
    ops = client.operations.operations_get(_from=yesterday.isoformat(), to=now.isoformat())
    print("operations")
    print(ops)
    print()


def print_orders():
    orders = client.orders.orders_get()
    print("active orders")
    print(orders)
    print()


def make_order():
    order_response = client.orders.orders_limit_order_post(figi='BBG009S39JX6',
                                                           limit_order_request={"lots": 1,
                                                                                "operation": "Buy",
                                                                                "price": 0.01})
    print("make order")
    print(order_response)
    print()
    return order_response


# won't work in sandbox - orders are being instantly executed
def cancel_order(order_id):
    cancellation_result = client.orders.orders_cancel_post(order_id=order_id)
    print("cancel order")
    print(cancellation_result)
    print()


# set_balance()
# print_24hr_operations()
# print_orders()
# order_response = make_order()
# print_orders()
# cancel_order(order_response.payload.order_id)
# print_orders()

# us = client.user.user_accounts_get()
# print(us)

# bnd = client.market.market_bonds_get(async_req=True)
bnd = client.market.market_stocks_get()
print(bnd)


'''
    пакет https://github.com/Awethon/open-api-python-client
    
    Создание клиента .. \open-api-python-client\openapi_client\
    openapi
        sandbox_api_client                  Тестовый клиент (тестовый токен)
        api_client                          клиент (токен)

    Файлы библиотек .. \open-api-python-client\openapi_genclient\api\
    user
        user_accounts_get                   Получение брокерских счетов клиента
    
    sandbox
        sandbox_clear_post                  Удаление всех позиций
        sandbox_currencies_balance_post     Выставление баланса по валютным позициям
        sandbox_positions_balance_post      Выставление баланса по инструментным позициям
        sandbox_register_post               Регистрация клиента в sandbox
        sandbox_remove_post                 Удаление счета
        
    portfolio
        portfolio_currencies_get            Получение валютных активов клиента
        portfolio_get                       Получение портфеля клиента
        
    orders
        orders_cancel_post                  Отмена заявки
        orders_get                          Получение списка активных заявок
        orders_limit_order_post             Создание лимитной заявки
        orders_market_order_post            Создание рыночной заявки
        
    operations
        operations_get                      Получение списка операций
    
    market
        market_bonds_get                    Получение списка облигаций
        market_candles_get                  Получение исторических свечей по FIGI
        market_currencies_get               Получение списка валютных пар
        market_etfs_get                     Получение списка ETF
        market_orderbook_get                Получение исторических стакана по FIGI
        market_search_by_figi_get           Получение инструмента по FIGI
        market_search_by_ticker_get         Получение инструмента по тикеру
        market_stocks_get                   Получение списка акций
'''