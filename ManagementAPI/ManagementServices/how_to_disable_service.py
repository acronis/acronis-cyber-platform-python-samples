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
    """Retrieves tenant information
    via the `/tenants/{tenant_id}` endpoint

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


def disable_service(client: Client, tenant_id: str, application_id: dict,
                    service_name: str) -> list:
    """Disables service for tenant

    :param client: Client object
    :param tenant_id: ID of tenant
    :param application_id: ID of application
    :param service_name: Name of service
    :return: information about disabled service
    """
    payload = dict(offering_items=list())
    items = get_offering_items(client, tenant_id)
    filtered_items = [item for item in items if
                      item['application_id'] == application_id and
                      item['name'] == service_name]
    for item in filtered_items:
        payload['offering_items'].append(dict(
            application_id=item['application_id'],
            name=item['name'], status=0))
    return offer_items(client, tenant_id, payload)[0]


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    disable_service(client, args.tenant_id, args.application_id,
                    args.service_name)


if __name__ == '__main__':
    args = parse_arguments('tenant-id', 'application-id', 'service-name')
    main(args)
