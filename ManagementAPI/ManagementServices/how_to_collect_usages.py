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


def get_usages(client: Client, tenant_ids: list) -> list:
    """Retrieves the service usages for tenants
    via the `/tenants/usages` endpoint

    :param client: Client object
    :param tenant_ids: IDs of tenants
    :return: Information about usages
    """
    response = requests.get(
        f'{client.base_url}/api/2/tenants/usages',
        headers=client.auth_header,
        params=dict(tenants=','.join(tenant_ids)),
    )
    handle_error_response(response)
    return response.json()['items']


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    usages = get_usages(client, [args.tenant_id])
    print(usages)


if __name__ == '__main__':
    args = parse_arguments('tenant-id')
    main(args)
