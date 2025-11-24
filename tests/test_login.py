import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_correct_login(api_login):
    request_context, headers = api_login
    response = request_context.get("api/v1.0/user-profiles?page=0&size=5&sort=id%2Cdesc", headers=headers)
    assert response.status == 200
