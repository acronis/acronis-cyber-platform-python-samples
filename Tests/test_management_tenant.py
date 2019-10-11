from ManagementAPI.ManagementTenant.how_to_create_tenant import create_tenant
from ManagementAPI.ManagementTenant.how_to_delete_tenant import delete_tenant
from ManagementAPI.ManagementTenant.how_to_disable_tenant import disable_tenant
from ManagementAPI.ManagementTenant.how_to_get_information_about_child_tenants import \
    get_child_info
from ManagementAPI.ManagementTenant.how_to_limit_access_to_tenant import \
    limit_access_to_tenant
from ManagementAPI.ManagementTenant.how_to_move_tenant_to_another_tenant import \
    move_tenant
from ManagementAPI.ManagementTenant.how_to_search_for_a_tenant_by_name import \
    get_tenants_by_name
from ManagementAPI.ManagementTenant.how_to_update_tenant import update_tenant
from ManagementAPI.ManagementTenant.how_to_update_tenant_pricing import \
    update_pricing_settings
from client import Client
from tools import GrantType


def test_create_and_delete_tenant():
    client = Client(grant_type=GrantType.client_credentials)
    new_tenant_data = dict(name='test', kind='partner')
    new_tenant = create_tenant(client, new_tenant_data.copy())
    assert new_tenant
    assert new_tenant['name'] == new_tenant_data['name']
    assert new_tenant['kind'] == new_tenant_data['kind']

    assert disable_tenant(client, new_tenant['id'])
    assert delete_tenant(client, new_tenant['id'])


def test_get_child_info(tenant):
    client = Client(grant_type=GrantType.client_credentials)
    child_info = get_child_info(client)
    assert child_info
    child_id = [item['id'] for item in child_info]
    assert tenant['id'] in child_id


def test_search_tenants_by_name(tenant):
    client = Client(grant_type=GrantType.client_credentials)
    response = get_tenants_by_name(client, tenant['name'])
    for item in response:
        assert item['obj_type'] == 'tenant' and tenant['name'] in item['name']


def test_limit_access_to_tenant():
    client = Client(grant_type=GrantType.client_credentials)
    assert limit_access_to_tenant(client)


def test_move_tenant(tenant, customer_tenant):
    client = Client(grant_type=GrantType.client_credentials)
    assert move_tenant(
        client, customer_tenant['id'],
        new_parent_id=tenant['id'],
    )


def test_update_tenant(tenant):
    def add_prefix(arg):
        return f'new_{arg}'

    client = Client(grant_type=GrantType.client_credentials)
    contact_data_keys = [
        'address1', 'address2', 'city', 'email', 'country',
        'firstname', 'lastname', 'phone', 'state', 'zipcode',
    ]
    contact_data = {key: add_prefix(key) for key in contact_data_keys}
    contact_data.update(email='test@mysite.com')

    data = dict(tenant_id=tenant['id'], name=add_prefix(tenant['name']))
    data.update(contact_data)

    tenant_info = update_tenant(client, tenant_data=data.copy())
    assert tenant_info
    assert tenant_info['id'] == data['tenant_id']
    assert tenant_info['name'] == data['name']
    for key in contact_data_keys:
        assert tenant_info['contact'][key] == data[key]


def test_switch_tenant_mode(tenant):
    client = Client(grant_type=GrantType.client_credentials)
    pricing_data = dict(tenant_id=tenant['id'], mode='trial')
    response = update_pricing_settings(client, pricing_data.copy())
    assert response
    assert response['mode'] == pricing_data['mode']


def test_update_pricing_settings(customer_tenant):
    client = Client(grant_type=GrantType.client_credentials)
    pricing_data = dict(
        tenant_id=customer_tenant['id'], mode='production', currency='USD',
    )
    response = update_pricing_settings(client, pricing_data.copy())
    assert response
    assert response['mode'] == pricing_data['mode']
    assert response['currency'] == pricing_data['currency']
