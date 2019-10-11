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


def activities_get(client: Client) -> dict:
    """Retrieves list of activities via
    the `/api/task_manager/v2/activities` endpoint

    :param client: Client object
    :return: information about activities
    """
    response = requests.get(
        f'{client.base_url}/api/task_manager/v2/activities',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()


def main():
    client = Client(grant_type=GrantType.password)

    result = activities_get(client)
    print(result)


if __name__ == "__main__":
    main()
