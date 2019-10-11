"""
@date 30.08.2019
@author Anna.Shavrina@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

from ManagementAPI.ManagementClient.how_to_create_client import create_client
from ManagementAPI.ManagementClient.how_to_delete_client import delete_client
from ManagementAPI.ManagementClient.how_to_retrieve_client_info import \
    get_client_info
from ManagementAPI.ManagementClient.how_to_update_client import update_client
from client import Client
from tools import GrantType


def test_create_and_delete_client():
    auth_client = Client(grant_type=GrantType.client_credentials)
    client_type = 'agent'
    client = create_client(auth_client, client_type)
    assert client['type'] == client_type
    assert delete_client(auth_client, client['client_id'])


def test_update_client_info(client):
    auth_client = Client(grant_type=GrantType.client_credentials)
    agent_type, hostname = 'BackUpAgent1', 'NewHost'
    client_info = update_client(
        auth_client, client['client_id'], agent_type, hostname,
    )
    assert client_info
    assert client_info['data']['hostname'] == hostname
    assert client_info['data']['agent_type'] == agent_type


def test_get_client_info(client):
    auth_client = Client(grant_type=GrantType.client_credentials)
    client_info = get_client_info(auth_client, client['client_id'])
    assert client_info['client_id'] == client['client_id']
