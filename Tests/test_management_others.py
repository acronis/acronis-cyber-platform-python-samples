import time

import requests

from ManagementAPI.ManagementTenant.how_to_disable_tenant import get_tenant_info
from ManagementAPI.Others.how_to_add_idp import add_idp, set_default_idp
from ManagementAPI.Others.how_to_add_storage import add_infra
from ManagementAPI.Others.how_to_collect_usage_by_report import \
    __get_stored_report, __get_report_status, __order_report
from client import Client
from tools import handle_error_response, GrantType


def test_idp(tenant):
    client = Client(grant_type=GrantType.client_credentials)

    idp_info = dict(
        owner_tenant_id=tenant['id'],
        oauth2_client_id='0' * 20,
        oauth2_client_secret='0' * 40,
        domain='ex.example.com',
        address='https://ex.example.com',
    )
    idp = add_idp(client, idp_info.copy())
    for key in idp_info.keys():
        assert idp[key] == idp_info[key]

    assert set_default_idp(client, tenant['id'], idp['id'])

    tenant_info = get_tenant_info(client, tenant['id'])
    assert tenant_info['default_idp_id'] == idp['id']


def test_storage(tenant_all_app_enabled):
    client = Client(grant_type=GrantType.client_credentials)

    infra_info = dict(
        owner_tenant_id=tenant_all_app_enabled['id'],
        name='test_storage',
        url='microsoft+azure://ex.test.com/',
    )
    infra = add_infra(client, infra_info)
    for key in infra_info.keys():
        assert infra[key] == infra_info[key]

    response = requests.get(
        f'{client.base_url}/api/2/infra/{infra["id"]}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    assert response.json()['id'] == infra['id']


def test_usages_by_report():
    client = Client(grant_type=GrantType.client_credentials)
    order = __order_report(client, client.tenant_id, ['json_v2_0'], 'save')

    status = __get_report_status(client, order['id'])
    while status['items'][0]['status'] != 'saved':
        status = __get_report_status(client, order['id'])
        time.sleep(1)
    assert __get_stored_report(client, order['id'], status['items'][0]['id'])
    response = requests.delete(
        f'{client.base_url}/api/2/reports/{order["id"]}',
        headers=client.auth_header,
        params=dict(version=order['version']),
    )
    handle_error_response(response)
    assert response.status_code == 204
