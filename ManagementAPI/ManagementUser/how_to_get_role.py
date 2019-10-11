import os
import sys

import requests

sys.path.append(os.path.abspath('../../'))
from client import Client
from tools import handle_error_response, parse_arguments, GrantType


def get_role(client: Client, user_id: str) -> str:
    """Returns user's role via `users/{user_id}/access_policies` endpoint.

    :param client: Client object
    :param user_id: The ID of the user account
    :return: The role of the user account
    """
    response = requests.get(
        f'{client.base_url}/api/2/users/{user_id}/access_policies',
        headers=client.auth_header,
    )
    handle_error_response(response)
    data = response.json()
    return data['items'][0]['role_id'] if data['items'] else 'user'


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    role = get_role(client, args.user_id)
    assert role in ['user', 'hci_admin', 'partner_admin']


if __name__ == '__main__':
    args = parse_arguments('user-id')
    main(args)
