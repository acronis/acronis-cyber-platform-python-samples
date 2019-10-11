from ManagementAPI.ManagementServices.how_to_collect_usages import get_usages
from ManagementAPI.ManagementServices.how_to_disable_service import \
    disable_service
from ManagementAPI.ManagementServices.how_to_enable_services_for_app import \
    enable_services_for_app
from ManagementAPI.ManagementServices.how_to_remove_app import \
    remove_application
from ManagementAPI.ManagementServices.how_to_retreive_offering_items import \
    get_offering_items
from ManagementAPI.ManagementServices.how_to_set_quotas import set_quotas
from client import Client
from tools import GrantType

APP_ID = '6e6d758d-8e74-3ae3-ac84-50eb0dff12eb'  # backup application id
SERVICE_NAME = 'vms'


def test_enable_app(tenant):
    client = Client(grant_type=GrantType.client_credentials)
    enable_services_for_app(client, tenant['id'], APP_ID)

    enabled_services = get_offering_items(client, tenant['id'])
    assert enabled_services
    for item in enabled_services:
        assert item['application_id'] == APP_ID


def test_remove_app(tenant_all_app_enabled):
    client = Client(grant_type=GrantType.client_credentials)
    tenant_id = tenant_all_app_enabled['id']
    assert remove_application(client, tenant_id, APP_ID)

    offering_items = get_offering_items(client, tenant_id)
    for item in offering_items:
        assert item['application_id'] != APP_ID


def test_disable_service(tenant_all_app_enabled):
    client = Client(grant_type=GrantType.client_credentials)
    tenant_id = tenant_all_app_enabled['id']
    disable_service(client, tenant_id, APP_ID, SERVICE_NAME)

    offering_items = get_offering_items(client, tenant_id)
    for item in offering_items:
        if item['name'] == SERVICE_NAME:
            assert item['status'] == 0


def test_set_upgrade_quotas(tenant_all_app_enabled):
    client = Client(grant_type=GrantType.client_credentials)
    tenant_id = tenant_all_app_enabled['id']
    value = 10  # soft quota
    overage = 20  # hard quota
    assert set_quotas(client, tenant_id, APP_ID, SERVICE_NAME, value, overage)

    offering_items = get_offering_items(client, tenant_id)
    for item in offering_items:
        if item['name'] == SERVICE_NAME:
            assert item['quota']['value'] == value
            assert item['quota']['overage'] == overage

    new_value = 20
    new_overage = 40
    assert set_quotas(
        client, tenant_id, APP_ID, SERVICE_NAME, new_value, new_overage,
    )

    offering_items = get_offering_items(client, tenant_id)
    for item in offering_items:
        if item['name'] == SERVICE_NAME:
            assert item['quota']['value'] == new_value
            assert item['quota']['overage'] == new_overage


def test_usages(tenant_all_app_enabled):
    client = Client(grant_type=GrantType.client_credentials)
    assert get_usages(client, [tenant_all_app_enabled['id']])
