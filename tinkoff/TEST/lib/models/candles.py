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


class Candles(object):
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
        'interval': 'CandleResolution',
        'candles': 'list[Candle]'
    }

    attribute_map = {
        'figi': 'figi',
        'interval': 'interval',
        'candles': 'candles'
    }

    def __init__(self, figi=None, interval=None, candles=None, local_vars_configuration=None):  # noqa: E501
        """Candles - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._figi = None
        self._interval = None
        self._candles = None
        self.discriminator = None

        self.figi = figi
        self.interval = interval
        self.candles = candles

    @property
    def figi(self):
        """Gets the figi of this Candles.  # noqa: E501


        :return: The figi of this Candles.  # noqa: E501
        :rtype: str
        """
        return self._figi

    @figi.setter
    def figi(self, figi):
        """Sets the figi of this Candles.


        :param figi: The figi of this Candles.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and figi is None:  # noqa: E501
            raise ValueError("Invalid value for `figi`, must not be `None`")  # noqa: E501

        self._figi = figi

    @property
    def interval(self):
        """Gets the interval of this Candles.  # noqa: E501


        :return: The interval of this Candles.  # noqa: E501
        :rtype: CandleResolution
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this Candles.


        :param interval: The interval of this Candles.  # noqa: E501
        :type: CandleResolution
        """
        if self.local_vars_configuration.client_side_validation and interval is None:  # noqa: E501
            raise ValueError("Invalid value for `interval`, must not be `None`")  # noqa: E501

        self._interval = interval

    @property
    def candles(self):
        """Gets the candles of this Candles.  # noqa: E501


        :return: The candles of this Candles.  # noqa: E501
        :rtype: list[Candle]
        """
        return self._candles

    @candles.setter
    def candles(self, candles):
        """Sets the candles of this Candles.


        :param candles: The candles of this Candles.  # noqa: E501
        :type: list[Candle]
        """
        if self.local_vars_configuration.client_side_validation and candles is None:  # noqa: E501
            raise ValueError("Invalid value for `candles`, must not be `None`")  # noqa: E501

        self._candles = candles

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
        if not isinstance(other, Candles):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Candles):
            return True

        return self.to_dict() != other.to_dict()
