from ManagementAPI.ManagementUser.how_to_change_user_password import \
    change_password
from ManagementAPI.ManagementUser.how_to_create_user import create_user
from ManagementAPI.ManagementUser.how_to_delete_user import delete_user
from ManagementAPI.ManagementUser.how_to_enable_disable_user import \
    enable_user, disable_user
from ManagementAPI.ManagementUser.how_to_get_role import get_role
from ManagementAPI.ManagementUser.how_to_search_user_by_login import \
    get_users_by_login
from ManagementAPI.ManagementUser.how_to_send_user_activation_email import \
    send_user_activation_email
from ManagementAPI.ManagementUser.how_to_set_role import set_role
from ManagementAPI.ManagementUser.how_to_update_user import update_user_info
from client import Client
from tools import GrantType


def test_change_password(child_user):
    client = Client(grant_type=GrantType.client_credentials)
    assert change_password(client, child_user['id'], 'testSECRETpassword123')


def test_create_and_delete_user():
    client = Client(grant_type=GrantType.client_credentials)
    new_user_data = dict(login='test_login', email='test_email@email.com')
    new_user = create_user(client, new_user_data.copy())
    assert new_user
    assert new_user['login'] == new_user_data['login']
    assert new_user['contact']['email'] == new_user_data['email']

    assert disable_user(client, new_user['id'])
    assert delete_user(client, new_user['id'])


def test_enable_and_disable_user(user):
    client = Client(grant_type=GrantType.client_credentials)
    assert disable_user(client, user_id=user['id'])
    assert enable_user(client, user_id=user['id'])


def test_get_role(user):
    client = Client(grant_type=GrantType.client_credentials)
    role = get_role(client, user_id=user['id'])
    assert role in ['user', 'hci_admin', 'partner_admin']


def test_search_user_by_login(user):
    client = Client(grant_type=GrantType.client_credentials)
    response = get_users_by_login(client, user['login'])
    for item in response:
        assert item['obj_type'] == 'user' and user['login'] in item['login']


def test_send_user_activation_email(child_user):
    client = Client(grant_type=GrantType.client_credentials)
    assert send_user_activation_email(client, child_user['id'])


def test_set_buyer_type(child_user):
    client = Client(grant_type=GrantType.client_credentials)
    user_data = dict(user_id=child_user['id'], set_buyer_type=1)
    response = update_user_info(client, user_data)
    assert response
    assert response['business_types'] == ['buyer']


def test_set_role(user):
    client = Client(grant_type=GrantType.client_credentials)
    role = 'hci_admin'
    assert set_role(client, user_id=user['id'], role=role)
    assert get_role(client, user_id=user['id']) == role


def test_update_user(user):
    def add_prefix(arg):
        return f'new_{arg}'

    client = Client(grant_type=GrantType.client_credentials)
    contact_data_keys = [
        'address1', 'address2', 'city', 'email', 'country',
        'firstname', 'lastname', 'phone', 'state', 'zipcode',
    ]
    contact_data = {key: add_prefix(key) for key in contact_data_keys}
    contact_data.update(email=add_prefix(user['contact']['email']))

    data = dict(user_id=user['id'], login=add_prefix(user['login']))
    data.update(contact_data)

    user_info = update_user_info(client, user_data=data.copy())
    assert user_info
    assert user_info['login'] == data['login']
    for key in contact_data_keys:
        assert user_info['contact'][key] == data[key]
