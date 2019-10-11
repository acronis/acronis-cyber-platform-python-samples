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
    """Retrieves tenant information via the `/tenants/{tenant_id}` endpoint

    :param client: Client object
    :param tenant_id: ID of tenant
    :return: Information about tenant
    """
    response = requests.get(
        f'{client.base_url}/api/2/tenants/{tenant_id}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()


def get_available_items(client: Client, tenant_id: str) -> list:
    """Retrieves list of items available to enable on this tenant's children
    via the `/tenants/{tenant_id}/offering_items/available_for_child` endpoint

    :param client: Client object
    :param tenant_id: ID of tenant
    :return: list of items
    """
    response = requests.get(
        f'{client.base_url}/api/2/tenants/'
        f'{tenant_id}/offering_items/available_for_child',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()['items']


def offer_items(client: Client, tenant_id: str, payload: dict) -> list:
    """Updates the list of services, quotas on other service parameters for
    tenant via the `/tenants/{tenant_id}/offering_items` endpoint

    :param client: Client object
    :param tenant_id: The ID of the tenant
    :param payload: Information about changing items
    :return: Information about updated items
    """
    response = requests.put(
        f'{client.base_url}/api/2/tenants/{tenant_id}/offering_items',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()['items']


def enable_services_for_app(client: Client, tenant_id: str,
                            application_id: str) -> list:
    """Enables application's services.

    :param client: Client object
    :param tenant_id: ID of tenant
    :param application_id: ID of application
    :return: The list of information about enabled services
    """
    tenant_info = get_tenant_info(client, tenant_id)
    available_items = get_available_items(client, tenant_info['parent_id'])
    offering_items = [item for item in available_items if
                      item['application_id'] == application_id]
    payload = dict(offering_items=offering_items)

    if not payload['offering_items']:
        raise Exception('Provided `application_id` not available')

    return offer_items(client, tenant_id, payload)


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    enable_services_for_app(client, args.tenant_id, args.application_id)


if __name__ == '__main__':
    args = parse_arguments('tenant-id', 'application-id')
    main(args)
