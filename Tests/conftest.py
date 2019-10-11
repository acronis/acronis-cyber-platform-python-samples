import os
import sys

import pytest

sys.path.append(os.path.abspath('../'))
from client import Client
from tools import GrantType
from Tests.test_alert_manager import delete_alert
from AlertManager.how_to_create_alert import create_alert
from DisasterRecovery.how_to_create_recovery_server import \
    create_recovery_server, get_networks, get_image_specs
from DisasterRecovery.how_to_delete_recovery_server import \
    delete_recovery_server
from ManagementAPI.ManagementUser.how_to_create_user import create_user
from ManagementAPI.ManagementUser.how_to_delete_user import delete_user
from ManagementAPI.ManagementUser.how_to_enable_disable_user import disable_user
from ManagementAPI.ManagementTenant.how_to_create_tenant import create_tenant
from ManagementAPI.ManagementTenant.how_to_disable_tenant import disable_tenant
from ManagementAPI.ManagementTenant.how_to_delete_tenant import delete_tenant
from ManagementAPI.ManagementClient.how_to_create_client import create_client
from ManagementAPI.ManagementClient.how_to_delete_client import delete_client
from ManagementAPI.ManagementServices.how_to_enable_services_for_app import \
    get_available_items, offer_items


@pytest.fixture
def user():
    client = Client(grant_type=GrantType.client_credentials)

    user_data = dict(login='test_login', email='test_email@email.com')
    user = create_user(client, user_data)
    yield user

    # teardown
    assert disable_user(client, user['id'])
    assert delete_user(client, user['id'])


@pytest.fixture
def child_user(customer_tenant):
    client = Client(grant_type=GrantType.client_credentials)

    user_data = dict(
        login='test_login',
        email='test_email@email.com',
        tenant_id=customer_tenant['id'],
    )
    user = create_user(client, user_data)
    yield user

    # teardown
    assert disable_user(client, user['id'])
    assert delete_user(client, user['id'])


@pytest.fixture
def tenant():
    client = Client(grant_type=GrantType.client_credentials)

    tenant_data = dict(kind='partner', name='test_name')
    tenant = create_tenant(client, tenant_data)
    yield tenant

    # teardown
    assert disable_tenant(client, tenant['id'])
    assert delete_tenant(client, tenant['id'])


@pytest.fixture
def customer_tenant():
    client = Client(grant_type=GrantType.client_credentials)

    tenant_data = dict(kind='customer', name='test_customer_name')
    tenant = create_tenant(client, tenant_data)
    yield tenant

    # teardown
    assert disable_tenant(client, tenant['id'])
    assert delete_tenant(client, tenant['id'])


@pytest.fixture
def tenant_all_app_enabled(tenant):
    client = Client(grant_type=GrantType.client_credentials)

    items = get_available_items(client, client.tenant_id)
    offer_items(client, tenant['id'], dict(offering_items=items))
    yield tenant


@pytest.fixture
def client():
    auth_client = Client(grant_type=GrantType.client_credentials)

    client = create_client(auth_client, client_type='agent')
    yield client

    # teardown
    assert delete_client(auth_client, client['client_id'])


@pytest.fixture
def alert():
    client = Client(grant_type=GrantType.password)

    alert = create_alert(client, dict(type='DrStorageHardQuotaExceeds'))
    yield alert

    # teardown
    assert delete_alert(client, alert)


@pytest.fixture
def recovery_server():
    client = Client(grant_type=GrantType.password, use_dr_config=True)

    server_data = dict(
        source='UBUNTU1604',
        name='test_name',
        description='test_decription',
        internetAccess=True,
        publicAddress=False,
    )

    # Get a list of available networks
    networks = get_networks(client)

    # Get a list of available image specifications
    image_specs = get_image_specs(client)

    server_data.update(network=networks[0], imageSpec=image_specs[0])

    recovery_server = create_recovery_server(client, server_data)
    assert recovery_server
    yield recovery_server

    # teardown
    assert delete_recovery_server(
        client, server_id=recovery_server['resourceId']
    )
