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


class OrdersResponse(object):
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
        'tracking_id': 'str',
        'status': 'str',
        'payload': 'list[Order]'
    }

    attribute_map = {
        'tracking_id': 'trackingId',
        'status': 'status',
        'payload': 'payload'
    }

    def __init__(self, tracking_id=None, status='Ok', payload=None, local_vars_configuration=None):  # noqa: E501
        """OrdersResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._tracking_id = None
        self._status = None
        self._payload = None
        self.discriminator = None

        self.tracking_id = tracking_id
        self.status = status
        self.payload = payload

    @property
    def tracking_id(self):
        """Gets the tracking_id of this OrdersResponse.  # noqa: E501


        :return: The tracking_id of this OrdersResponse.  # noqa: E501
        :rtype: str
        """
        return self._tracking_id

    @tracking_id.setter
    def tracking_id(self, tracking_id):
        """Sets the tracking_id of this OrdersResponse.


        :param tracking_id: The tracking_id of this OrdersResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and tracking_id is None:  # noqa: E501
            raise ValueError("Invalid value for `tracking_id`, must not be `None`")  # noqa: E501

        self._tracking_id = tracking_id

    @property
    def status(self):
        """Gets the status of this OrdersResponse.  # noqa: E501


        :return: The status of this OrdersResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this OrdersResponse.


        :param status: The status of this OrdersResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def payload(self):
        """Gets the payload of this OrdersResponse.  # noqa: E501


        :return: The payload of this OrdersResponse.  # noqa: E501
        :rtype: list[Order]
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """Sets the payload of this OrdersResponse.


        :param payload: The payload of this OrdersResponse.  # noqa: E501
        :type: list[Order]
        """
        if self.local_vars_configuration.client_side_validation and payload is None:  # noqa: E501
            raise ValueError("Invalid value for `payload`, must not be `None`")  # noqa: E501

        self._payload = payload

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
        if not isinstance(other, OrdersResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrdersResponse):
            return True

        return self.to_dict() != other.to_dict()
