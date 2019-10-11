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


def delete_user(client: Client, user_id: str) -> bool:
    """Deletes disabled user account via the `/users/{user_id}` endpoint.

    :param client: Client object
    :param user_id: The ID of the user account
    :return: `True` if succeeded, `False` otherwise
    """
    params = {'version': get_user_info(client, user_id)['version']}
    response = requests.delete(
        f'{client.base_url}/api/2/users/{user_id}',
        headers=client.auth_header,
        params=params,
    )
    handle_error_response(response)
    return response.status_code == 204


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    assert delete_user(client, args.user_id)


if __name__ == '__main__':
    args = parse_arguments('user-id')
    main(args)
