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
from tools import handle_error_response, GrantType


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


def limit_access_to_tenant(client: Client) -> bool:
    """Limits access to tenant via the `/tenants/{tenant_id}` endpoint.
    
    :param client: Client object
    :return: `True` if succeeded, `False` otherwise
    """
    tenant_id = client.tenant_id
    payload = {
        'tenant_id': tenant_id,
        'ancestral_access': False,
        'version': get_tenant_info(client, tenant_id)['version'],
    }

    response = requests.put(
        f"{client.base_url}/api/2/tenants/{tenant_id}",
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()['ancestral_access'] is False


def main():
    client = Client(grant_type=GrantType.client_credentials)

    assert limit_access_to_tenant(client)


if __name__ == '__main__':
    main()
