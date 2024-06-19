import json

from tests.data.party_data import party_raw


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    result = MockResponse(None, 404)
    if args[0] == 'https://api.oireachtas.ie/v1/parties?chamber_id=&chamber=dail&house_no=33&limit=5000':
        result = MockResponse(json.loads(party_raw), 200)

    return result
