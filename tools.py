"""
@date 30.08.2019
@author Roman.Detinin@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

import argparse
import json
from enum import Enum, auto

import requests


class GrantType(Enum):
    password = auto()
    client_credentials = auto()


def parse_arguments(*args):
    parser = argparse.ArgumentParser()
    for arg in args:
        (arg_name, required) = arg if type(arg) is tuple else (arg, True)
        parser.add_argument(f'--{arg_name}', required=required)
    return parser.parse_args()


def handle_error_response(response: requests.Response):
    """Extends exception handling of the response.

    :param response: Response object of the "Requests" library
    :raises requests.HTTPError: Raises error code exception
    """
    try:
        response.raise_for_status()
    except requests.HTTPError:
        #  TODO: This can be logged
        #  TODO: Better handling of different errors and status codes
        if response.status_code in (400, 404, 405, 409):
            print('An HTTP error has occurred.')
            print('See details below:')
            try:
                error = response.json()['error']
                print(f'Error code: {error["code"]}\n'
                      f'Message: {error["message"]}\n'
                      f'Details: {error["details"]}')
            except json.decoder.JSONDecodeError:
                print(response.text)
            except KeyError:
                print(response.json())
        else:
            try:
                print(response.json())
            except json.decoder.JSONDecodeError:
                print(response.text)
            print('=' * len('Traceback (most recent call last):'))
        raise


def clean_arguments(args: dict) -> dict:
    """Cleans up a dictionary from keys containing value `None`.

    :param args: A dictionary of argument/value pairs generated with ArgumentParser
    :return: A dictionary with argument/value pairs without `None` values
    :rtype: dict
    """
    rv = {}
    for (key, val) in args.items():
        if isinstance(val, dict):
            val = clean_arguments(val) or None
        if val is not None:
            rv[key] = val
    return rv
