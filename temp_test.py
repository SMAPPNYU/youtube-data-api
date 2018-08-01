import pytest
import requests
from unittest import mock

@mock.patch('requests.get')
def test_verify(mock_request):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 404

    mock_request.return_value = mock_resp
    r = requests.get()
    #print(r.status_code)

    with pytest.raises(requests.exceptions.HTTPError) as err_msg:
        r.raise_for_status()
    print(err_msg)
