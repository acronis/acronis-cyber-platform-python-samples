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


def get_children(client: Client, tenant_id: str) -> list:
    """Retrieves children of a given tenant
    via the `/tenants/{tenant_id}/children` endpoint
    
    :param client: Client object
    :param tenant_id: Tenant ID string
    :return: A dictionary with tenant children IDs
    """
    response = requests.get(
        f'{client.base_url}/api/2/tenants/{tenant_id}/children',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()['items']


def get_tenants_info(client: Client, tenants: list) -> list:
    """Retrieves the information of a given tenants batch
    via the `/tenants` endpoint
    
    :param client: Client object
    :param tenants: list of Tenant IDs
    :return: A list with tenants information
    """
    response = requests.get(
        f'{client.base_url}/api/2/tenants',
        headers=client.auth_header,
        params=dict(uuids=','.join(tenants)),
    )
    handle_error_response(response)
    return response.json()['items']


def get_child_info(client: Client, tenant_id: str = None) -> list:
    """Retrieves information about child tenants of a given tenant
    
    :param client: Client object
    :param tenant_id: Tenant ID string
    :return: A dictionary with child tenants information
    """
    tenant_id = tenant_id or client.tenant_id
    children = get_children(client, tenant_id)
    return get_tenants_info(client, children)


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    response = get_child_info(client, args.tenant_id)
    print(response)


if __name__ == '__main__':
    args = parse_arguments(('tenant-id', False))
    main(args)
