"""
@date 30.08.2019
@author Faeel.Zaripov@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

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


def get_tenants_by_name(client: Client, name: str,
                        tenant_id: str = None, limit: int = 10) -> list:
    """Searches tenants by name via the `/search` endpoint.

    :param client: Client object
    :param name: A name to search in tenants
    :param tenant_id: Tenant ID string
    :param limit: Limits the amount of the results. Default = 10
    :return: A list with tenants information
    """
    items = search(client, text=name, tenant_id=tenant_id, limit=limit)
    return [
        item for item in items if
        item['obj_type'] == 'tenant' and name in item['name']
    ]


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    result = get_tenants_by_name(client, args.name, args.tenant_id)
    print(result)


if __name__ == '__main__':
    args = parse_arguments(('name', True), ('tenant-id', False))
    main(args)
