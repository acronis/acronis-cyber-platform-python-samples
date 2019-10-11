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
from tools import handle_error_response, parse_arguments, clean_arguments, \
    GrantType


def get_user_info(client: Client, user_id: str) -> dict:
    """Retrieves the information about the user account
    via the `/users/{user_id}` endpoint.

    :param client: Client object
    :param user_id: The ID of the user account
    :return: A dictionary with the user account information
    """
    response = requests.get(
        f'{client.base_url}/api/2/users/{user_id}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.json()


def update_user_info(client: Client, user_data: dict) -> dict:
    """Updates a user account via the `/users/{user_id}` endpoint.
    To set `buyer` type for customer's user account
    use option --set-buyer-type 1

    :param client: Client object
    :param user_data: User account information to update
    :return: A dictionary with updated user account information
    """
    user_id = user_data.get('user_id')

    payload = {
        'version': get_user_info(client, user_id)['version'],
        'login': user_data.get('login'),
        'contact': {
            'email': user_data.get('email'),
            'address1': user_data.get('address1'),
            'address2': user_data.get('address2'),
            'state': user_data.get('state'),
            'zipcode': user_data.get('zipcode'),
            'city': user_data.get('city'),
            'country': user_data.get('country'),
            'phone': user_data.get('phone'),
            'firstname': user_data.get('firstname'),
            'lastname': user_data.get('lastname'),
        }
    }

    if user_data.get('set_buyer_type'):
        payload['business_types'] = ['buyer']

    payload = clean_arguments(payload)

    response = requests.put(
        f'{client.base_url}/api/2/users/{user_id}',
        headers=client.auth_header,
        json=payload,
    )
    handle_error_response(response)
    return response.json()


def main(args):
    client = Client(grant_type=GrantType.client_credentials)

    # Convert ArgumentParser namespace object to a dictionary
    user_data = clean_arguments(vars(args))

    result = update_user_info(client, user_data)
    print(result)


if __name__ == '__main__':
    args = parse_arguments(('user-id', True),
                           ('login', False),
                           ('address1', False),
                           ('address2', False),
                           ('city', False),
                           ('country', False),
                           ('email', False),
                           ('firstname', False),
                           ('lastname', False),
                           ('phone', False),
                           ('state', False),
                           ('zipcode', False),
                           ('set-buyer-type', False))
    main(args)
