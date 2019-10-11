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


def tasks_get(client: Client) -> list:
    """Retrieve tasks via the `/api/task_manager/v2/tasks` endpoint

    :param client: Client object
    :return: List of information about tasks
    """
    response = requests.get(
        f'{client.base_url}/api/task_manager/v2/tasks',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()["items"]


def main():
    client = Client(grant_type=GrantType.password)

    result = tasks_get(client)
    print(result)


if __name__ == '__main__':
    main()
