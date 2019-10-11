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


def get_offered_items(client: Client, tenant_id: str) -> list:
    """Retrieves the information about services for tenant
    via the `/tenants/{tenant_id}/offering_items` endpoint

    :param client: Client object
    :param tenant_id: The ID of the tenant
    :return: Information about services
    """
    response = requests.get(
        f'{client.base_url}/api/2/tenants/{tenant_id}/offering_items',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()['items']


def set_quotas(client: Client, tenant_id: str, application_id: str,
               service_name: str, value: int, overage: int) -> list:
    """Change the quotas of service for tenant

    :param client: Client object
    :param tenant_id: The ID of the tenant
    :param application_id: The ID of application
    :param service_name: The name of service
    :param value: Soft quota value
    :param overage: The hard quota value
    :return: Information about updated items
    """
    items = get_offered_items(client, tenant_id)
    offering_items = [item for item in items if
                      item['application_id'] == application_id and
                      item['name'] == service_name]
    payload = dict(offering_items=offering_items)

    if not payload['offering_items']:
        raise Exception('Provided `application_id` and '
                        '`name` of service not available')
    if payload['offering_items'][0]['status'] == 0:
        raise Exception('Service is disabled on the tenant')
    payload['offering_items'][0]['quota']['value'] = value
    payload['offering_items'][0]['quota']['overage'] = overage
    return offer_items(client, tenant_id, payload)


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    set_quotas(
        client, args.tenant_id, args.application_id,
        args.service_name, int(args.value), int(args.overage)
    )


if __name__ == '__main__':
    args = parse_arguments('tenant-id', 'application-id',
                           'service-name', 'value', 'overage')
    main(args)
