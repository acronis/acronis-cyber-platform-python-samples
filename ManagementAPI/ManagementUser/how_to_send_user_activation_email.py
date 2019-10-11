import os
import sys

import requests

sys.path.append(os.path.abspath('../../'))
from client import Client
from tools import handle_error_response, parse_arguments, GrantType


def send_user_activation_email(client: Client, user_id: str) -> bool:
    """Sends activation e-mail to user
    via the `/users/{user_id}/send-activation-email` endpoint.

    In case of customer tenant this function is available only for
    users of child tenants

    In case of partner tenant this function is available only for
    users of child tenants with role 'partner_admin' (Administrator)

    :param client: Client object
    :param user_id: The ID of the user account
    :return: `True` if succeeded, `False` otherwise
    """
    response = requests.post(
        f'{client.base_url}/api/2/users/{user_id}/send-activation-email',
        headers=client.auth_header,
        json={},
    )
    handle_error_response(response)
    return response.status_code == 204


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    assert send_user_activation_email(client, args.user_id)


if __name__ == '__main__':
    args = parse_arguments('user-id')
    main(args)
