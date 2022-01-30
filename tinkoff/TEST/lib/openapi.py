from .api.market_api import MarketApi
from .api.operations_api import OperationsApi
from .api.orders_api import OrdersApi
from .api.portfolio_api import PortfolioApi
from .api.sandbox_api import SandboxApi
from .api.user_api import UserApi
from .api_client import ApiClient
from .configuration import Configuration


class SandboxOpenApi(object):
    def __init__(self, api_client):
        self.sandbox = SandboxApi(api_client=api_client)
        self.orders = OrdersApi(api_client=api_client)
        self.portfolio = PortfolioApi(api_client=api_client)
        self.market = MarketApi(api_client=api_client)
        self.operations = OperationsApi(api_client=api_client)
        self.user = UserApi(api_client=api_client)


class OpenApi(object):
    def __init__(self, api_client):
        self.orders = OrdersApi(api_client=api_client)
        self.portfolio = PortfolioApi(api_client=api_client)
        self.market = MarketApi(api_client=api_client)
        self.operations = OperationsApi(api_client=api_client)
        self.user = UserApi(api_client=api_client)


def sandbox_api_client(token):
    sandbox_host = 'https://api-invest.tinkoff.ru/openapi/sandbox/'
    conf = Configuration(host=sandbox_host)

    conf.access_token = token
    return SandboxOpenApi(ApiClient(configuration=conf))


def api_client(token):
    host = 'https://api-invest.tinkoff.ru/openapi/'
    conf = Configuration(host=host)
    conf.access_token = token
    return OpenApi(ApiClient(configuration=conf))

