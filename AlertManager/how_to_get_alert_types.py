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
from tools import handle_error_response, GrantType


def get_alert_types(client: Client) -> list:
    """Retrieves alert types via the `/api/alert_manager/v1/types` endpoint

    :param client: Client object
    :return: list of Alert types
    """
    response = requests.get(
        f'{client.base_url}/api/alert_manager/v1/types',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()['items']


def main():
    client = Client(grant_type=GrantType.password)
    result = get_alert_types(client)
    print(result)


if __name__ == '__main__':
    main()
