from TaskManager.how_to_get_activities import activities_get
from TaskManager.how_to_get_task import task_get
from TaskManager.how_to_get_tasks import tasks_get
from client import Client
from tools import GrantType


def test_get_activities():
    client = Client(grant_type=GrantType.password)
    assert activities_get(client)


def test_get_tasks():
    client = Client(grant_type=GrantType.password)
    tasks = tasks_get(client)
    assert tasks is not None
    if tasks:
        assert task_get(client, tasks[0]['id'])
