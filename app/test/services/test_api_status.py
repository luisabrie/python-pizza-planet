import pytest

def test_get_status(client, status_uri):
    response = client.get(f'{status_uri}')
    pytest.assume(response.status.startswith('200'))
    pytest.assume(response.json['status'] == 'up')
