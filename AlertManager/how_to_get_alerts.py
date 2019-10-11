"""
@date 30.08.2019
@author Roman.Detinin@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

import os
import sys

import requests

sys.path.append(os.path.abspath('../'))
from client import Client
from tools import handle_error_response, GrantType


def get_alerts(client: Client) -> list:
    """Retrieves alerts via the `/api/alert_manager/v1/alerts` endpoint

    :param client: Client object
    :return: List of alerts
    """
    response = requests.get(
        f'{client.base_url}/api/alert_manager/v1/alerts',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()['items']


def main():
    client = Client(grant_type=GrantType.password)

    result = get_alerts(client)
    print(result)


if __name__ == '__main__':
    main()
