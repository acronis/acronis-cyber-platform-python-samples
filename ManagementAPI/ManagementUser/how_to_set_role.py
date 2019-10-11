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
from tools import handle_error_response, parse_arguments, GrantType


def set_role(client: Client, user_id: str, role: str,
             id: str = '00000000-0000-0000-0000-000000000000',
             issuer_id: str = '00000000-0000-0000-0000-000000000000',
             trustee_type: str = 'user', version: int = 0) -> bool:
    """Sets the role for user account
    via the `users/{user_id}/access_policies` endpoint.

    :param client: Client object
    :param user_id: The ID of the user account
    :param role: one of the following:
        `user`          - Regular user
        `hci_admin`     - Cyber Infrastructure
        `partner_admin` - Administrator
    :param id: TODO
    :param issuer_id: TODO
    :param trustee_type: TODO
    :param version: User account revision number
    :return: `True` if succeeded, `False` otherwise
    """

    if role in ['user']:
        payload = {'items': []}
    elif role in ['hci_admin', 'partner_admin']:
        payload = {
            'items': [
                {
                    'id': id,
                    'issuer_id': issuer_id,
                    'role_id': role,
                    'tenant_id': client.tenant_id,
                    'trustee_id': user_id,
                    'trustee_type': trustee_type,
                    'version': version,
                }
            ]
        }
    else:
        raise Exception('Wrong value for `role`')

    response = requests.put(
        f'{client.base_url}/api/2/users/{user_id}/access_policies',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.status_code == 200


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    assert set_role(client, args.user_id, args.role)


if __name__ == '__main__':
    args = parse_arguments('user-id', 'role')
    main(args)
