"""
@date 30.08.2019
@author Anna.Shavrina@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

import os
import sys

import requests

sys.path.append(os.path.abspath('../../'))
from client import Client
from tools import handle_error_response, parse_arguments, GrantType


def get_user_info(client: Client, user_id: str) -> dict:
    """Retrieves the information about the user account
    via the `/users/{user_id}` endpoint.

    :param client: Client object
    :param user_id: The ID of the user account
    :return: A dictionary with the user account information
    """
    response = requests.get(
        f'{client.base_url}/api/2/users/{user_id}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()


def change_password(client: Client, user_id: str, password: str) -> bool:
    """Changes password for child user account
    via the `/users/{user_id}/password` endpoint.

    :param client: Client object
    :param user_id: The ID of the user account
    :param password: New password
    :return: `True` if succeeded, `False` otherwise
    """
    payload = {
        'version': get_user_info(client, user_id)['version'],
        'password': password,
    }

    response = requests.post(
        f'{client.base_url}/api/2/users/{user_id}/password',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.status_code == 204


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    assert change_password(client, args.user_id, args.password)


if __name__ == '__main__':
    args = parse_arguments('user-id', 'password')
    main(args)
