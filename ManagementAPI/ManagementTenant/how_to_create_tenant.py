"""
@date 30.08.2019
@author Roman.Detinin@acronis.com
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


def create_tenant(client: Client, tenant_data: dict) -> dict:
    """Creates a new tenant via the `/tenants` endpoint.
    To create tenant in trial mode use kind=customer

    :param client: Client object
    :param tenant_data: Tenant information
    :return: A dictionary with tenant information
    """
    payload = {
        'parent_id': tenant_data.get('parent_id', client.tenant_id),
        'name': tenant_data.get('name'),
        'kind': tenant_data.get('kind'),
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
        'language': tenant_data.get('language', 'en'),
        'customer-id': tenant_data.get('customer-id'),
        'internal-tag': tenant_data.get('internal-tag'),
    }

    payload = clean_arguments(payload)

    response = requests.post(
        f'{client.base_url}/api/2/tenants',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    # Convert ArgumentParser namespace object to a dictionary
    tenant_data = clean_arguments(vars(args))

    result = create_tenant(client, tenant_data)
    print(result)


if __name__ == "__main__":
    args = parse_arguments(("name", True),
                           ("kind", True),
                           ("parent-id", False),
                           ("address1", False),
                           ("address2", False),
                           ("city", False),
                           ("country", False),
                           ("email", False),
                           ("firstname", False),
                           ("lastname", False),
                           ("phone", False),
                           ("state", False),
                           ("zipcode", False),
                           ("customer-id", False),
                           ("internal-tag", False),
                           ("language", False))
    main(args)
