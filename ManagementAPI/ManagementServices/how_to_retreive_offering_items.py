"""
@date 30.08.2019
@author Faeel.Zaripov@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

import os
import sys

import requests

sys.path.append(os.path.abspath('../..'))
from tools import parse_arguments
from client import Client
from tools import handle_error_response, GrantType


def get_offering_items(client: Client, tenant_id: str = None) -> list:
    """Retrieves the information about services for tenant
    via the `/tenants/{tenant_id}/offering_items` endpoint

    :param client: Client object
    :param tenant_id: The ID of the tenant
    :return: Information about services
    """
    tenant_id = tenant_id or client.tenant_id
    response = requests.get(
        f'{client.base_url}/api/2/tenants/{tenant_id}/offering_items',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()['items']


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    items = get_offering_items(client, args.tenant_id)
    print(items)


if __name__ == '__main__':
    args = parse_arguments(('tenant-id', False))
    main(args)
