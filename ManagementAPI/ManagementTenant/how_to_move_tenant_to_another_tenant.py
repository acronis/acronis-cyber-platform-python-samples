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


def get_tenant_info(client: Client, tenant_id: str) -> dict:
    """Retrieves the information about the tenant
    via the `/tenants/{tenant_id}` endpoint.

    :param client: Client object
    :param tenant_id: The ID of the tenant
    :return: A dictionary with the tenant information
    """
    response = requests.get(
        f'{client.base_url}/api/2/tenants/{tenant_id}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()


def move_tenant(client: Client, tenant_id: str, new_parent_id: str) -> bool:
    """Moves tenant to another tenant via the `/tenants/{tenant_id}` endpoint
    
    :param client: Client object
    :param tenant_id: Tenant ID string
    :param new_parent_id: Parent tenant ID string
    :return: `True` if succeeded, `False` otherwise
    """
    payload = {
        'tenant_id': tenant_id,
        'parent_id': new_parent_id,
        'version': get_tenant_info(client, tenant_id)['version'],
    }

    response = requests.put(
        f'{client.base_url}/api/2/tenants/{tenant_id}',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()['parent_id'] == new_parent_id


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    assert move_tenant(client, args.tenant_id, args.new_parent_id)


if __name__ == '__main__':
    args = parse_arguments(('tenant-id', True), ('new-parent-id', True))
    main(args)
