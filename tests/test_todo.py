def test_create_todo(client,token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}' },
        json = {
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )
    assert response.json() == {
        'title': 'Test todo',
        'id': 1,
        'description': 'Test todo description',
        'state': 'draft',
    }