import os
import sys

import requests

sys.path.append(os.path.abspath('../../'))
from client import Client
from tools import handle_error_response, parse_arguments, GrantType


def search(client: Client, text: str,
           tenant_id: str = None, limit: int = 10) -> list:
    """Searches tenants and users via the `/search` endpoint.

    :param client: Client object
    :param text: A text to search in tenants and users
    :param tenant_id: Tenant ID string
    :param limit: Limits the amount of the results. Default = 10
    :return: A list with the results
    """
    params = {
        'tenant': tenant_id or client.tenant_id,
        'text': text,
        'limit': limit,
    }
    response = requests.get(
        f'{client.base_url}/api/2/search',
        headers=client.auth_header,
        params=params,
    )
    handle_error_response(response)
    return response.json()['items']


def get_users_by_login(client: Client, login: str,
                       tenant_id: str = None, limit: int = 10) -> list:
    """Searches users via the `/search` endpoint.

    :param client: Client object
    :param login: A login to search in users
    :param tenant_id: Tenant ID string
    :param limit: Limits the amount of the results. Default = 10
    :return: A list with the results
    """
    items = search(client, text=login, tenant_id=tenant_id, limit=limit)
    return [item for item in items if item['obj_type'] == 'user']


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    result = get_users_by_login(client, args.login, args.tenant_id, args.limit)
    print(result)


if __name__ == '__main__':
    args = parse_arguments(('login', True),
                           ('tenant-id', False),
                           ('limit', False))
    main(args)
