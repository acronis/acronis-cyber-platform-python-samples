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
from tools import handle_error_response, parse_arguments, clean_arguments, \
    GrantType


def create_alert(client: Client, alert_data: dict) -> dict:
    """Creates new alert via the `/api/alert_manager/v1/alerts` endpoint

    :param client: Client object
    :param alert_data: Alert information
    :return: Information about created alert
    """
    payload = {
        'type': alert_data.get('type'),
        'activityId': alert_data.get('activityId'),
        'archiveName': alert_data.get('archiveName'),
        'resourceId': alert_data.get('resourceId'),
        'commandId': alert_data.get('commandId'),
        'planId': alert_data.get('planId'),
        'licenseName': alert_data.get('licenseName'),
        'actionName': alert_data.get('actionName'),
        'runbookName': alert_data.get('runbookName'),
        'stepName': alert_data.get('stepName'),
        'uri': alert_data.get('uri'),
        'what': alert_data.get('what'),
        'resourceType': alert_data.get('resourceType'),
    }

    payload = clean_arguments(payload)

    response = requests.post(
        f'{client.base_url}/api/alert_manager/v1/alerts',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()


def main(args):
    client = Client(grant_type=GrantType.password)

    # Convert ArgumentParser namespace object to a dictionary
    alert_data = clean_arguments(vars(args))

    result = create_alert(client, alert_data)
    print(result)


if __name__ == '__main__':
    args = parse_arguments(('type', True),
                           ('activityId', False),
                           ('archiveName', False),
                           ('resourceId', False),
                           ('commandId', False),
                           ('planId', False),
                           ('licenseName', False),
                           ('actionName', False),
                           ('runbookName', False),
                           ('stepName', False),
                           ('uri', False),
                           ('what', False),
                           ('resourceType', False))
    main(args)
