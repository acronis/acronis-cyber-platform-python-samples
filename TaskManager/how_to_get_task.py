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
from tools import handle_error_response, parse_arguments, GrantType


def task_get(client: Client, task_id: str) -> dict:
    """Retrieves task by it's id
    via the `/api/task_manager/v2/tasks/{task_id}` endpoint

    :param client: Client object
    :param task_id:
    :return: Information about activity
    """
    response = requests.get(
        f'{client.base_url}/api/task_manager/v2/tasks/{task_id}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()


def main(args):
    client = Client(grant_type=GrantType.password)

    result = task_get(client, args.task_id)
    print(result)


if __name__ == '__main__':
    args = parse_arguments('task-id')
    main(args)
