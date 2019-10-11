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


def remove_application(client: Client, tenant_id: str,
                       application_id: str) -> bool:
    """Remove application from tenant via the
    `/applications/{application_id}/bindings/tenants/{tenant_id}` endpoint

    :param client: Client object
    :param tenant_id: ID of tenant
    :param application_id: ID of application
    :return: `True` if succeeded, `False` otherwise
    """
    response = requests.delete(
        f'{client.base_url}/api/2/applications/{application_id}'
        f'/bindings/tenants/{tenant_id}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.status_code == 204


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    assert remove_application(client, args.tenant_id, args.application_id)


if __name__ == '__main__':
    args = parse_arguments('tenant-id', 'application-id')
    main(args)
