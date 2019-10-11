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


def update_tenant(client: Client, tenant_data: dict) -> dict:
    """Updates tenant information via the `/tenants/{tenant_id}` endpoint.
    
    :param client: Client object
    :param tenant_data: Tenant information to update
    :return: A dictionary with updated information
    """
    tenant_id = tenant_data.get('tenant_id')

    payload = {
        'contact': {
            'address1': tenant_data.get('address1'),
            'address2': tenant_data.get('address2'),
            'city': tenant_data.get('city'),
            'country': tenant_data.get('country'),
            'email': tenant_data.get('email'),
            'firstname': tenant_data.get('firstname'),
            'lastname': tenant_data.get('lastname'),
            'phone': tenant_data.get('phone'),
            'state': tenant_data.get('state'),
            'zipcode': tenant_data.get('zipcode'),
        },
        'customer-id': tenant_data.get('customer-id'),
        'customer-type': tenant_data.get('customer-type'),
        'enabled': tenant_data.get('enabled'),
        'internal-tag': tenant_data.get('internal-tag'),
        'kind': tenant_data.get('kind'),
        'language': tenant_data.get('language'),
        'name': tenant_data.get('name'),
        'ancestral-access': tenant_data.get('ancestral-access'),
        'parent-id': tenant_data.get('parent-id'),
        'version': get_tenant_info(client, tenant_id)['version'],
    }

    payload = clean_arguments(payload)

    response = requests.put(
        f'{client.base_url}/api/2/tenants/{tenant_id}',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    # Convert ArgumentParser namespace object to a dictionary
    tenant_data = clean_arguments(vars(args))

    response = update_tenant(client, tenant_data)
    print(response)


if __name__ == '__main__':
    args = parse_arguments(('tenant-id', True),
                           ('address1', False),
                           ('address2', False),
                           ('city', False),
                           ('country', False),
                           ('email', False),
                           ('firstname', False),
                           ('lastname', False),
                           ('phone', False),
                           ('state', False),
                           ('zipcode', False),
                           ('customer-id', False),
                           ('customer-type', False),
                           ('default-idp-id', False),
                           ('enabled', False),
                           ('internal-tag', False),
                           ('kind', False),
                           ('language', False),
                           ('name', False),
                           ('ancestral-access', False),
                           ('parent-id', False))
    main(args)
