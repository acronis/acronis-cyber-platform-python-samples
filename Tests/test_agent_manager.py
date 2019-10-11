"""
@date 30.08.2019
@author Anna.Shavrina@acronis.com
@details  :copyright: 2003–2019 Acronis International GmbH,
Rheinweg 9, 8200 Schaffhausen, Switzerland. All rights reserved.
"""

from AgentManager.how_to_get_list_of_agents import get_agents
from client import Client
from tools import GrantType


def test_get_list():
    client = Client(grant_type=GrantType.password)
    assert get_agents(client)
