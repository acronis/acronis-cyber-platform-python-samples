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


def delete_tenant(client: Client, tenant_id: str) -> bool:
    """Deletes the tenant via the `/tenants/{tenant_id}` endpoint

    :param client: Client object
    :param tenant_id: The ID of the tenant
    :return: `True` if succeeded, `False` otherwise
    """
    params = {'version': get_tenant_info(client, tenant_id)['version']}
    response = requests.delete(
        f'{client.base_url}/api/2/tenants/{tenant_id}',
        headers=client.auth_header,
        params=params,
    )
    handle_error_response(response)
    return response.status_code == 204


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    assert delete_tenant(client, args.tenant_id)


if __name__ == '__main__':
    args = parse_arguments(('tenant-id', True))
    main(args)
