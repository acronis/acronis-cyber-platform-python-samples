import requests

from AlertManager.how_to_create_alert import create_alert
from AlertManager.how_to_get_alert_by_id import get_alert
from AlertManager.how_to_get_alert_type_by_id import get_alert_type
from AlertManager.how_to_get_alert_types import get_alert_types
from AlertManager.how_to_get_alerts import get_alerts
from client import Client
from tools import handle_error_response, GrantType


def delete_alert(client, alert):
    response = requests.delete(
        f'{client.base_url}/api/alert_manager/v1/alerts/{alert["id"]}',
        headers=client.auth_header,
    )
    handle_error_response(response)
    return response.status_code == 204


def test_create_and_delete_alert():
    client = Client(grant_type=GrantType.password)
    alert = create_alert(client, dict(type='DrStorageHardQuotaExceeds'))
    assert alert
    assert delete_alert(client, alert)


def test_get_alerts():
    client = Client(grant_type=GrantType.password)
    assert get_alerts(client) is not None


def test_get_alert(alert):
    client = Client(grant_type=GrantType.password)
    alert_info = get_alert(client, alert['id'])
    assert alert_info
    assert alert['id'] == alert_info['id']


def test_alert_types():
    client = Client(grant_type=GrantType.password)
    alert_types = get_alert_types(client)
    assert alert_types is not None
    if alert_types:
        assert get_alert_type(client, alert_types[0]['id'])
