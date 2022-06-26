import requests
from hamcrest import *

bin_name = "stuart"
payload = {
    "data": {
        "schedulePackage": {
            "success": True,
            "error": None,
            "package": {
                "id": "12345",
                "deliveries": [
                    {
                        "tasks": [
                            {
                                "type": "PICKUP",
                                "address": {
                                    "geocoded": "Carrer de Pau Claris 130, 08009, Barcelona, Spain",
                                    "location": {
                                        "lat": "41.39317",
                                        "long": "2.16699"
                                    }
                                }
                            },
                            {
                                "type": "DROPOFF",
                                "address": {
                                    "geocoded": "Carrer de Pau Claris 170, 08037, Barcelona, Spain",
                                    "location": {
                                        "lat": "41.39546",
                                        "long": "2.16385"
                                    }
                                }
                            }
                        ]
                    }
                ],
                "status": "NOT_ASSIGNED",
                "createdAt": "2022-03-23T15:06:09+01:00",
                "ref": "67890"
            }
        }
    }
}


def before_all(context):
    """
    Run before the tests
    - create a named bin
    - post the webhook to the bin
    """
    uri = context.config.userdata.get("endpoint", "http://localhost:9000")
    context.vars = {'uri': uri, 'bin_name': bin_name}

    if requests.get('{}/{}'.format(context.vars['uri'], context.vars['bin_name'])).status_code != 200:
        create_bin = requests.post('{}/api/v1/bins'.format(context.vars['uri']), data={"given_name": bin_name})
        assert_that(create_bin.status_code, equal_to(200))

    webhook = requests.post('{}/{}'.format(context.vars['uri'], context.vars['bin_name']), json=payload)
    assert_that(webhook.status_code, equal_to(200))
