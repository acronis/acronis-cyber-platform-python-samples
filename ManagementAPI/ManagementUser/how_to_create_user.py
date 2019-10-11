"""
@date 30.08.2019
@author Roman.Detinin@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

import os
import sys

import requests

sys.path.append(os.path.abspath('../../'))
from client import Client
from tools import handle_error_response, parse_arguments, clean_arguments, \
    GrantType


def is_login_free(client: Client, login: str) -> bool:
    """Checks if login is free via the `/users/check_login` endpoint.

    :param client: Client object
    :param login: login to check
    :return: `True` if login is free, `False` otherwise
    """
    response = requests.get(
        f'{client.base_url}/api/2/users/check_login',
        params={'username': login},
        headers=client.auth_header,
    )
    return response.status_code == 204


def create_user(client: Client, user_data: dict) -> dict:
    """Creates a new user via the `/users` endpoint.

    :param client: Client object
    :param user_data: User account information
    :return: A dictionary with user account information
    """
    if not is_login_free(client, user_data.get('login')):
        return {'error': 'User with this login already exists!'}

    payload = {
        'tenant_id': user_data.get('tenant_id', client.tenant_id),
        'login': user_data.get('login'),
        'contact': {
            'login': user_data.get('login'),
            'email': user_data.get('email'),
            'address1': user_data.get('address1'),
            'address2': user_data.get('address2'),
            'state': user_data.get('state'),
            'zipcode': user_data.get('zipcode'),
            'city': user_data.get('city'),
            'phone': user_data.get('phone'),
            'firstname': user_data.get('firstname'),
            'lastname': user_data.get('lastname'),
        },
    }

    response = requests.post(
        f'{client.base_url}/api/2/users',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    # Convert ArgumentParser namespace object to a dictionary
    user_data = clean_arguments(vars(args))

    result = create_user(client, user_data)
    print(result)


if __name__ == '__main__':
    args = parse_arguments(('login', True),
                           ('email', True),
                           ('tenant-id', False),
                           ('address1', False),
                           ('address2', False),
                           ('state', False),
                           ('zipcode', False),
                           ('city', False),
                           ('phone', False),
                           ('firstname', False),
                           ('lastname', False))
    main(args)
