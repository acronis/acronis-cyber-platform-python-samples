"""
@date 30.08.2019
@author Roman.Detinin@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

import json
import logging
import os

import requests
from jsonschema import validate
from requests.auth import HTTPBasicAuth

from tools import GrantType
from tools import handle_error_response

logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'samples.log'),
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
)


#  OPTIONAL: These are sample exceptions, which can be more
#  descriptive in the context of our library and API.
class ClientException(Exception):
    """Base exception for client"""
    pass


class EmptyCredentials(ClientException):
    """Exception for client credentials"""
    pass


class InvalidGrantType(ClientException):
    """Exception for invalid grant type"""
    pass


#  OPTIONAL: There can be even more complex implementation
#  with several types of clients.
class Client:
    """Represents a user account or client.

    :param grant_type: Authorization grant type
    :raises EmptyCredentials: Empty credentials provided in config
    :raises InvalidGrantType: Invalid grant type provided
    """

    #  OPTIONAL:
    #  https://docs.python.org/3/reference/datamodel.html#slots
    __slots__ = (
        '_login', '_password', '_client_id', '_client_secret', '_router_url',
        '_base_url', '_auth_header', '_tenant_id', '_config', '_grant_type',
    )

    #  TODO: Maybe a user can provide a path to
    #   the configuration file by himself.
    def __init__(self, grant_type, use_dr_config=False, use_grpm_config=False):

        #  Read the configuration file and store it in a variable
        config_name = 'config.json'

        if use_grpm_config:
            config_name = 'grpm_' + config_name
        elif use_dr_config:
            config_name = 'dr_' + config_name

        self._config = self._read_config(
            os.path.join(os.path.dirname(__file__), config_name)
        )

        #  Define API router url
        #  By default it will lead to the beta cloud (for development purposes)
        self._router_url = self._config.get('router_url')

        #  The grant type will be used to check if proper
        #  grant type is used to access certain method.
        self._grant_type = grant_type

        #  Login is required to get base url to the API
        self._login = self._config.get('login')
        if not self._login:
            # This exception is mandatory for the production environment
            raise EmptyCredentials(
                'A login must be provided in order to get the base url.'
            )

        #  Send a request to the router url to get the login-specific
        #  server url (for production environment)
        response = requests.get(
            self._router_url,
            verify=not use_grpm_config,
            params=dict(login=self._login),
        )
        handle_error_response(response)

        #  Form base_url based on received server_url
        self._base_url = response.json().get("server_url")

        payload = dict(grant_type=self._grant_type.name, scope='openid')

        if self._grant_type == GrantType.password:

            #  Get the password from the config
            self._password = self._config.get('password')
            if not self._password:
                raise EmptyCredentials(
                    'Password is not provided in the configuration file.'
                )

            payload.update(
                dict(
                    username=self._login,
                    password=self._password,
                    scope='offline_access',
                )
            )
            auth = None

        elif self._grant_type == GrantType.client_credentials:

            #  Get the client_id and client_secret which are necessary
            #  for 'client_credentials' grant_type
            self._client_id = self._config.get('client_id')
            self._client_secret = self._config.get('client_secret')
            if not self._client_id or not self._client_secret:
                raise EmptyCredentials(
                    'Client ID and/or client secret are '
                    'not provided in the configuration file.'
                )
            auth = HTTPBasicAuth(self._client_id, self._client_secret)

        else:
            raise InvalidGrantType('Incorrect grant_type provided.')

        response = requests.post(
            f'{self.base_url}/api/2/idp/token',
            verify=not use_grpm_config,
            auth=auth,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=payload,
        )
        handle_error_response(response)

        access_token = response.json().get('access_token')
        #  Generate authorization header for further use in the requests
        self._auth_header = dict(Authorization=f'Bearer {access_token}')

        #  OPTIONAL: Create and store more properties
        #  of the client here if necessary
        response = requests.get(
            f'{self.base_url}/api/2/users/me',
            verify=not use_grpm_config,
            headers=self._auth_header,
        )
        handle_error_response(response)
        self._tenant_id = response.json().get('tenant_id')

    #  Functions and variables starting with '_' are
    #  meant for internal use only.
    def _read_config(self, config_path: str) -> dict:
        """Opens a JSON configuration file and converts
        its content into a dictionary.

        :param config_path: Path to JSON configuration file
        :return: A dictionary with configuration data
        :rtype: dict
        """
        config_schema = {
            'type': 'object',
            'properties': {
                'login': {'type': 'string'},
                'password': {'type': 'string'},
                'router_url': {'type': 'string'},
                'client_id': {'type': 'string'},
                'client_secret': {'type': 'string'},
            },
            'required': [
                'login', 'password', 'router_url', 'client_id', 'client_secret'
            ]
        }
        with open(config_path) as config_file:
            config = json.load(config_file)

        validate(instance=config, schema=config_schema)
        return config

    #  These are class properties which can hold any
    #  read-only values or computable values.
    @property
    def tenant_id(self):
        return self._tenant_id

    @property
    def base_url(self):
        return self._base_url

    @property
    def auth_header(self):
        return self._auth_header
