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


class MarketOrderRequest(object):
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
        'lots': 'int',
        'operation': 'OperationType'
    }

    attribute_map = {
        'lots': 'lots',
        'operation': 'operation'
    }

    def __init__(self, lots=None, operation=None, local_vars_configuration=None):  # noqa: E501
        """MarketOrderRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._lots = None
        self._operation = None
        self.discriminator = None

        self.lots = lots
        self.operation = operation

    @property
    def lots(self):
        """Gets the lots of this MarketOrderRequest.  # noqa: E501


        :return: The lots of this MarketOrderRequest.  # noqa: E501
        :rtype: int
        """
        return self._lots

    @lots.setter
    def lots(self, lots):
        """Sets the lots of this MarketOrderRequest.


        :param lots: The lots of this MarketOrderRequest.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and lots is None:  # noqa: E501
            raise ValueError("Invalid value for `lots`, must not be `None`")  # noqa: E501

        self._lots = lots

    @property
    def operation(self):
        """Gets the operation of this MarketOrderRequest.  # noqa: E501


        :return: The operation of this MarketOrderRequest.  # noqa: E501
        :rtype: OperationType
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """Sets the operation of this MarketOrderRequest.


        :param operation: The operation of this MarketOrderRequest.  # noqa: E501
        :type: OperationType
        """
        if self.local_vars_configuration.client_side_validation and operation is None:  # noqa: E501
            raise ValueError("Invalid value for `operation`, must not be `None`")  # noqa: E501

        self._operation = operation

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
        if not isinstance(other, MarketOrderRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MarketOrderRequest):
            return True

        return self.to_dict() != other.to_dict()