from http import HTTPStatus

from tests.conftest import VlanFactory




def test_create_vlan(client,token):
    response = client.post(
        '/vlans/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            
            "vlan": 223,
            "network": "192.168.21.0",
            "netmask": "255.255.255.0",
            "gateway": "192.168.21.1",
            "description": "Rede de Banco de dados",        
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
            "id": 1,
            "vlan": 223,
            "network": "192.168.21.0",            
        }


def test_list_vlans_return_5_vlans(session,client,token,user):
    expect_vlans = 5
    session.bulk_save_objects(
        VlanFactory.create_batch(5,user_id=user.id)
    )
    session.commit()
    


    response = client.get(
        '/vlans',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['vlans']) == expect_vlans