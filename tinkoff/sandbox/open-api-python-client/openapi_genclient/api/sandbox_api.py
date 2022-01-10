# coding: utf-8

"""
    OpenAPI

    tinkoff.ru/invest OpenAPI.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: n.v.melnikov@tinkoff.ru
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from openapi_genclient.api_client import ApiClient
from openapi_genclient.exceptions import (
    ApiTypeError,
    ApiValueError
)


class SandboxApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def sandbox_clear_post(self, **kwargs):  # noqa: E501
        """Удаление всех позиций  # noqa: E501

        Удаление всех позиций клиента  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_clear_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str broker_account_id: Номер счета (по умолчанию - Тинькофф)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Empty
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sandbox_clear_post_with_http_info(**kwargs)  # noqa: E501

    def sandbox_clear_post_with_http_info(self, **kwargs):  # noqa: E501
        """Удаление всех позиций  # noqa: E501

        Удаление всех позиций клиента  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_clear_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str broker_account_id: Номер счета (по умолчанию - Тинькофф)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Empty, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['broker_account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sandbox_clear_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'broker_account_id' in local_var_params and local_var_params['broker_account_id'] is not None:  # noqa: E501
            query_params.append(('brokerAccountId', local_var_params['broker_account_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['sso_auth']  # noqa: E501

        return self.api_client.call_api(
            '/sandbox/clear', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Empty',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sandbox_currencies_balance_post(self, sandbox_set_currency_balance_request, **kwargs):  # noqa: E501
        """Выставление баланса по валютным позициям  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_currencies_balance_post(sandbox_set_currency_balance_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param SandboxSetCurrencyBalanceRequest sandbox_set_currency_balance_request: Запрос на выставление баланса по валютным позициям (required)
        :param str broker_account_id: Номер счета (по умолчанию - Тинькофф)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Empty
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sandbox_currencies_balance_post_with_http_info(sandbox_set_currency_balance_request, **kwargs)  # noqa: E501

    def sandbox_currencies_balance_post_with_http_info(self, sandbox_set_currency_balance_request, **kwargs):  # noqa: E501
        """Выставление баланса по валютным позициям  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_currencies_balance_post_with_http_info(sandbox_set_currency_balance_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param SandboxSetCurrencyBalanceRequest sandbox_set_currency_balance_request: Запрос на выставление баланса по валютным позициям (required)
        :param str broker_account_id: Номер счета (по умолчанию - Тинькофф)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Empty, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sandbox_set_currency_balance_request', 'broker_account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sandbox_currencies_balance_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sandbox_set_currency_balance_request' is set
        if self.api_client.client_side_validation and ('sandbox_set_currency_balance_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['sandbox_set_currency_balance_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sandbox_set_currency_balance_request` when calling `sandbox_currencies_balance_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'broker_account_id' in local_var_params and local_var_params['broker_account_id'] is not None:  # noqa: E501
            query_params.append(('brokerAccountId', local_var_params['broker_account_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'sandbox_set_currency_balance_request' in local_var_params:
            body_params = local_var_params['sandbox_set_currency_balance_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['sso_auth']  # noqa: E501

        return self.api_client.call_api(
            '/sandbox/currencies/balance', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Empty',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sandbox_positions_balance_post(self, sandbox_set_position_balance_request, **kwargs):  # noqa: E501
        """Выставление баланса по инструментным позициям  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_positions_balance_post(sandbox_set_position_balance_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param SandboxSetPositionBalanceRequest sandbox_set_position_balance_request: Запрос на выставление баланса по инструментным позициям (required)
        :param str broker_account_id: Номер счета (по умолчанию - Тинькофф)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Empty
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sandbox_positions_balance_post_with_http_info(sandbox_set_position_balance_request, **kwargs)  # noqa: E501

    def sandbox_positions_balance_post_with_http_info(self, sandbox_set_position_balance_request, **kwargs):  # noqa: E501
        """Выставление баланса по инструментным позициям  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_positions_balance_post_with_http_info(sandbox_set_position_balance_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param SandboxSetPositionBalanceRequest sandbox_set_position_balance_request: Запрос на выставление баланса по инструментным позициям (required)
        :param str broker_account_id: Номер счета (по умолчанию - Тинькофф)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Empty, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sandbox_set_position_balance_request', 'broker_account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sandbox_positions_balance_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sandbox_set_position_balance_request' is set
        if self.api_client.client_side_validation and ('sandbox_set_position_balance_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['sandbox_set_position_balance_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sandbox_set_position_balance_request` when calling `sandbox_positions_balance_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'broker_account_id' in local_var_params and local_var_params['broker_account_id'] is not None:  # noqa: E501
            query_params.append(('brokerAccountId', local_var_params['broker_account_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'sandbox_set_position_balance_request' in local_var_params:
            body_params = local_var_params['sandbox_set_position_balance_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['sso_auth']  # noqa: E501

        return self.api_client.call_api(
            '/sandbox/positions/balance', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Empty',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sandbox_register_post(self, **kwargs):  # noqa: E501
        """Регистрация клиента в sandbox  # noqa: E501

        Создание счета и валютных позиций для клиента  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_register_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param SandboxRegisterRequest sandbox_register_request: Запрос на создание счета и выставление баланса по валютным позициям
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SandboxRegisterResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sandbox_register_post_with_http_info(**kwargs)  # noqa: E501

    def sandbox_register_post_with_http_info(self, **kwargs):  # noqa: E501
        """Регистрация клиента в sandbox  # noqa: E501

        Создание счета и валютных позиций для клиента  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_register_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param SandboxRegisterRequest sandbox_register_request: Запрос на создание счета и выставление баланса по валютным позициям
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SandboxRegisterResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sandbox_register_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sandbox_register_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'sandbox_register_request' in local_var_params:
            body_params = local_var_params['sandbox_register_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['sso_auth']  # noqa: E501

        return self.api_client.call_api(
            '/sandbox/register', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SandboxRegisterResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sandbox_remove_post(self, **kwargs):  # noqa: E501
        """Удаление счета  # noqa: E501

        Удаление счета клиента  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_remove_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str broker_account_id: Номер счета (по умолчанию - Тинькофф)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Empty
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sandbox_remove_post_with_http_info(**kwargs)  # noqa: E501

    def sandbox_remove_post_with_http_info(self, **kwargs):  # noqa: E501
        """Удаление счета  # noqa: E501

        Удаление счета клиента  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sandbox_remove_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str broker_account_id: Номер счета (по умолчанию - Тинькофф)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Empty, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['broker_account_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sandbox_remove_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'broker_account_id' in local_var_params and local_var_params['broker_account_id'] is not None:  # noqa: E501
            query_params.append(('brokerAccountId', local_var_params['broker_account_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['sso_auth']  # noqa: E501

        return self.api_client.call_api(
            '/sandbox/remove', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Empty',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
