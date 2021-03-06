"""
@date 30.08.2019
@author Faeel.Zaripov@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

import os
import sys

import requests

sys.path.append(os.path.abspath('../'))
from client import Client
from tools import handle_error_response, parse_arguments, GrantType


def get_alert_type(client: Client, type_id: str) -> dict:
    """Retrieves alert_type by id
    via the `/api/alert_manager/v1/types/{type_id}` endpoint

    :param client: Client object
    :param type_id: ID of alert-type
    :return: Information about alert_type
    """
    response = requests.get(
        f'{client.base_url}/api/alert_manager/v1/types/{type_id}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()


def main(args):
    client = Client(grant_type=GrantType.password)

    result = get_alert_type(client, args.type_id)
    print(result)


if __name__ == '__main__':
    args = parse_arguments('type-id')
    main(args)
