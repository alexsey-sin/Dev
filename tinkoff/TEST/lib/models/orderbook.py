# coding: utf-8

"""
    OpenAPI

    tinkoff.ru/invest OpenAPI.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: n.v.melnikov@tinkoff.ru
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ..configuration import Configuration


class Orderbook(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'figi': 'str',
        'depth': 'int',
        'bids': 'list[OrderResponse]',
        'asks': 'list[OrderResponse]',
        'trade_status': 'TradeStatus',
        'min_price_increment': 'float',
        'face_value': 'float',
        'last_price': 'float',
        'close_price': 'float',
        'limit_up': 'float',
        'limit_down': 'float'
    }

    attribute_map = {
        'figi': 'figi',
        'depth': 'depth',
        'bids': 'bids',
        'asks': 'asks',
        'trade_status': 'tradeStatus',
        'min_price_increment': 'minPriceIncrement',
        'face_value': 'faceValue',
        'last_price': 'lastPrice',
        'close_price': 'closePrice',
        'limit_up': 'limitUp',
        'limit_down': 'limitDown'
    }

    def __init__(self, figi=None, depth=None, bids=None, asks=None, trade_status=None, min_price_increment=None, face_value=None, last_price=None, close_price=None, limit_up=None, limit_down=None, local_vars_configuration=None):  # noqa: E501
        """Orderbook - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._figi = None
        self._depth = None
        self._bids = None
        self._asks = None
        self._trade_status = None
        self._min_price_increment = None
        self._face_value = None
        self._last_price = None
        self._close_price = None
        self._limit_up = None
        self._limit_down = None
        self.discriminator = None

        self.figi = figi
        self.depth = depth
        self.bids = bids
        self.asks = asks
        self.trade_status = trade_status
        self.min_price_increment = min_price_increment
        if face_value is not None:
            self.face_value = face_value
        if last_price is not None:
            self.last_price = last_price
        if close_price is not None:
            self.close_price = close_price
        if limit_up is not None:
            self.limit_up = limit_up
        if limit_down is not None:
            self.limit_down = limit_down

    @property
    def figi(self):
        """Gets the figi of this Orderbook.  # noqa: E501


        :return: The figi of this Orderbook.  # noqa: E501
        :rtype: str
        """
        return self._figi

    @figi.setter
    def figi(self, figi):
        """Sets the figi of this Orderbook.


        :param figi: The figi of this Orderbook.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and figi is None:  # noqa: E501
            raise ValueError("Invalid value for `figi`, must not be `None`")  # noqa: E501

        self._figi = figi

    @property
    def depth(self):
        """Gets the depth of this Orderbook.  # noqa: E501


        :return: The depth of this Orderbook.  # noqa: E501
        :rtype: int
        """
        return self._depth

    @depth.setter
    def depth(self, depth):
        """Sets the depth of this Orderbook.


        :param depth: The depth of this Orderbook.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and depth is None:  # noqa: E501
            raise ValueError("Invalid value for `depth`, must not be `None`")  # noqa: E501

        self._depth = depth

    @property
    def bids(self):
        """Gets the bids of this Orderbook.  # noqa: E501


        :return: The bids of this Orderbook.  # noqa: E501
        :rtype: list[OrderResponse]
        """
        return self._bids

    @bids.setter
    def bids(self, bids):
        """Sets the bids of this Orderbook.


        :param bids: The bids of this Orderbook.  # noqa: E501
        :type: list[OrderResponse]
        """
        if self.local_vars_configuration.client_side_validation and bids is None:  # noqa: E501
            raise ValueError("Invalid value for `bids`, must not be `None`")  # noqa: E501

        self._bids = bids

    @property
    def asks(self):
        """Gets the asks of this Orderbook.  # noqa: E501


        :return: The asks of this Orderbook.  # noqa: E501
        :rtype: list[OrderResponse]
        """
        return self._asks

    @asks.setter
    def asks(self, asks):
        """Sets the asks of this Orderbook.


        :param asks: The asks of this Orderbook.  # noqa: E501
        :type: list[OrderResponse]
        """
        if self.local_vars_configuration.client_side_validation and asks is None:  # noqa: E501
            raise ValueError("Invalid value for `asks`, must not be `None`")  # noqa: E501

        self._asks = asks

    @property
    def trade_status(self):
        """Gets the trade_status of this Orderbook.  # noqa: E501


        :return: The trade_status of this Orderbook.  # noqa: E501
        :rtype: TradeStatus
        """
        return self._trade_status

    @trade_status.setter
    def trade_status(self, trade_status):
        """Sets the trade_status of this Orderbook.


        :param trade_status: The trade_status of this Orderbook.  # noqa: E501
        :type: TradeStatus
        """
        if self.local_vars_configuration.client_side_validation and trade_status is None:  # noqa: E501
            raise ValueError("Invalid value for `trade_status`, must not be `None`")  # noqa: E501

        self._trade_status = trade_status

    @property
    def min_price_increment(self):
        """Gets the min_price_increment of this Orderbook.  # noqa: E501

        Шаг цены  # noqa: E501

        :return: The min_price_increment of this Orderbook.  # noqa: E501
        :rtype: float
        """
        return self._min_price_increment

    @min_price_increment.setter
    def min_price_increment(self, min_price_increment):
        """Sets the min_price_increment of this Orderbook.

        Шаг цены  # noqa: E501

        :param min_price_increment: The min_price_increment of this Orderbook.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and min_price_increment is None:  # noqa: E501
            raise ValueError("Invalid value for `min_price_increment`, must not be `None`")  # noqa: E501

        self._min_price_increment = min_price_increment

    @property
    def face_value(self):
        """Gets the face_value of this Orderbook.  # noqa: E501

        Номинал для облигаций  # noqa: E501

        :return: The face_value of this Orderbook.  # noqa: E501
        :rtype: float
        """
        return self._face_value

    @face_value.setter
    def face_value(self, face_value):
        """Sets the face_value of this Orderbook.

        Номинал для облигаций  # noqa: E501

        :param face_value: The face_value of this Orderbook.  # noqa: E501
        :type: float
        """

        self._face_value = face_value

    @property
    def last_price(self):
        """Gets the last_price of this Orderbook.  # noqa: E501


        :return: The last_price of this Orderbook.  # noqa: E501
        :rtype: float
        """
        return self._last_price

    @last_price.setter
    def last_price(self, last_price):
        """Sets the last_price of this Orderbook.


        :param last_price: The last_price of this Orderbook.  # noqa: E501
        :type: float
        """

        self._last_price = last_price

    @property
    def close_price(self):
        """Gets the close_price of this Orderbook.  # noqa: E501


        :return: The close_price of this Orderbook.  # noqa: E501
        :rtype: float
        """
        return self._close_price

    @close_price.setter
    def close_price(self, close_price):
        """Sets the close_price of this Orderbook.


        :param close_price: The close_price of this Orderbook.  # noqa: E501
        :type: float
        """

        self._close_price = close_price

    @property
    def limit_up(self):
        """Gets the limit_up of this Orderbook.  # noqa: E501

        Верхняя граница цены  # noqa: E501

        :return: The limit_up of this Orderbook.  # noqa: E501
        :rtype: float
        """
        return self._limit_up

    @limit_up.setter
    def limit_up(self, limit_up):
        """Sets the limit_up of this Orderbook.

        Верхняя граница цены  # noqa: E501

        :param limit_up: The limit_up of this Orderbook.  # noqa: E501
        :type: float
        """

        self._limit_up = limit_up

    @property
    def limit_down(self):
        """Gets the limit_down of this Orderbook.  # noqa: E501

        Нижняя граница цены  # noqa: E501

        :return: The limit_down of this Orderbook.  # noqa: E501
        :rtype: float
        """
        return self._limit_down

    @limit_down.setter
    def limit_down(self, limit_down):
        """Sets the limit_down of this Orderbook.

        Нижняя граница цены  # noqa: E501

        :param limit_down: The limit_down of this Orderbook.  # noqa: E501
        :type: float
        """

        self._limit_down = limit_down

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Orderbook):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Orderbook):
            return True

        return self.to_dict() != other.to_dict()