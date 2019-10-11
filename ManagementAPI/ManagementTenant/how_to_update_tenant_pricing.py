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
from tools import handle_error_response, parse_arguments, clean_arguments, \
    GrantType


def get_pricing_settings(client: Client, tenant_id: str) -> dict:
    """ Retrieves pricing settings for tenant via the
    `/tenants/{tenant_id}/pricing` endpoint

    :param client: Client object
    :param tenant_id: The ID of the tenant
    :return: A dictionary with the tenant's pricing settings
    """
    response = requests.get(
        f'{client.base_url}/api/2/tenants/{tenant_id}/pricing',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()


def update_pricing_settings(client: Client, pricing_data: dict) -> dict:
    """Updates tenant pricing via the `/tenants/{tenant_id}/pricing` endpoint.
    To switch tenant mode set `mode` argument to `production` or `trial`.
    
    :param client: Client object
    :param pricing_data: New pricing information
    :return: A dictionary with updated pricing
    """
    tenant_id = pricing_data.get('tenant_id')
    payload = {
        'version': get_pricing_settings(client, tenant_id)['version'],
        'mode': pricing_data.get('mode'),
        'currency': pricing_data.get('currency'),
    }

    payload = clean_arguments(payload)

    response = requests.put(
        f'{client.base_url}/api/2/tenants/{tenant_id}/pricing',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    # Convert ArgumentParser namespace object to a dictionary
    pricing_data = clean_arguments(vars(args))

    response = update_pricing_settings(client, pricing_data)
    print(response)


if __name__ == '__main__':
    args = parse_arguments(('tenant-id', True),
                           ('mode', False),
                           ('currency', False))
    main(args)
