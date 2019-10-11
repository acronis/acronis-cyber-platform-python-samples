import requests

from DisasterRecovery.how_to_activate_dr_in_vpn_less_mode import \
    activate_dr_in_vpn_less_mode
from DisasterRecovery.how_to_create_recovery_server import \
    create_recovery_server, get_networks, get_image_specs
from DisasterRecovery.how_to_delete_recovery_server import \
    delete_recovery_server
from DisasterRecovery.how_to_get_dr_status import get_dr_status_per_server
from DisasterRecovery.how_to_get_recovery_servers_listing import \
    get_recovery_servers_listing
from DisasterRecovery.how_to_read_recovery_server import read_recovery_server
from DisasterRecovery.how_to_update_recovery_server import \
    update_recovery_server
from client import Client
from tools import GrantType


def test_create_and_delete_recovery_server():
    client = Client(grant_type=GrantType.password, use_dr_config=True)

    server_data = dict(
        source='UBUNTU1604',
        name='test_name',
        description='test_decription',
        internetAccess=True,
        publicAddress=False,
        network=get_networks(client)[0],
        imageSpec=get_image_specs(client)[0],
    )

    server = create_recovery_server(client, server_data)
    assert server

    server_id = server['resourceId']
    server_info = read_recovery_server(client, server_id)
    assert server_info
    server_data.pop('publicAddress')
    for key in server_data:
        if key == 'source':
            assert server_data['source'] == server_info['recovery']['source']
        elif key == 'imageSpec':
            assert server_data['imageSpec'] == server_info['imageSpec']['id']
        else:
            assert server_data[key] == server_info[key]

    assert delete_recovery_server(client, server_id)


def test_activate_dr_in_vpn_less_mode():
    client = Client(grant_type=GrantType.password, use_dr_config=True)

    assert activate_dr_in_vpn_less_mode(client)
    response = requests.get(
        f'{client.base_url}/api/dr/v1/vpn/server',
        headers=client.auth_header,
    )
    assert response.json()['mode'] == 'customer-router-l2'


def test_get_dr_status_per_server(recovery_server):
    client = Client(grant_type=GrantType.password, use_dr_config=True)

    response = get_dr_status_per_server(client)
    assert response
    for item in response:
        assert item['id']
        assert item['drStatus']


def test_get_recovery_servers_listing(recovery_server):
    client = Client(grant_type=GrantType.password, use_dr_config=True)

    response = get_recovery_servers_listing(client)
    assert response
    for item in response:
        assert item['type'] == 'RECOVERY'
    server_ids = [item['id'] for item in response]
    assert recovery_server['resourceId'] in server_ids


def test_update_recovery_server(recovery_server):
    client = Client(grant_type=GrantType.password, use_dr_config=True)

    server_id = recovery_server['resourceId']
    server_data = dict(
        server_id=server_id,
        description='new_test_description',
        internetAccess=True,
        name='new_test_name',
        network=get_networks(client)[0],
        imageSpec=get_image_specs(client)[0],
    )

    updated_server = update_recovery_server(client, server_data)
    assert updated_server

    server_info = read_recovery_server(client, server_id)
    assert server_info
    for key in server_data:
        if key == 'imageSpec':
            assert server_data['imageSpec'] == server_info['imageSpec']['id']
        elif key == 'server_id':
            assert server_data['server_id'] == server_info['id']
        else:
            assert server_data[key] == server_info[key]
