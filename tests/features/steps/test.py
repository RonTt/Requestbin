from behave import *
from hamcrest import *
import requests
import json

use_step_matcher("re")


@given('The webhooks from a bin')
def step_get_webhook(context):
    """Get webhooks from bin, wait 5 secs to connect and 10 to receive the data"""
    try:
        res = requests.get('{}/api/v1/bins/{}/requests'.format(context.vars['uri'], context.vars['bin_name']),
                           timeout=(5, 10))
        assert_that(res.status_code, equal_to(200))
    except requests.exceptions.ReadTimeout:
        raise "Webhook not available after 10 seconds"

    webhook_ids = []

    for req in res.json():
        if 'id' in req:
            webhook_ids.append(req['id'])
    context.vars['ids'] = webhook_ids


@when('I get the content of them')
def step_get_content(context):
    """Get body of the webhooks"""
    body = []
    for idx in context.vars['ids']:
        res = requests.get('{}/api/v1/bins/{}/requests/{}'.format(context.vars['uri'], context.vars['bin_name'], idx))
        assert_that(res.status_code, equal_to(200))

        if res.json()['content_length'] > 0:
            print(idx)
            body.append(json.loads(res.json()['body']))
    context.vars['body'] = body


@then('I check that in the "{name}" the key "{expected_value}" is present')
def step_check_body(context, name, expected_value):
    """Check that the body contains a specific key"""
    for datas in context.vars['body']:
        assert_that(datas[name], has_key(expected_value))


@then('I check that in (?P<name>.*) (?P<key>.*) (?P<check>is|is not) (?P<expected_value>.*)')
def step_check_data(context, name, key, check, expected_value):
    """Check key are present and have a specific value"""
    for val in context.vars['body']:
        if name in val['data']:
            assert_that(val['data'][name], has_key(key))
            if check == "is":
                assert_that(str(val['data'][name][key]), equal_to(expected_value))
            else:
                assert str(val['data'][name][key]) != expected_value


@then('I check that (?P<key>.*) type in (?P<name>.*) (?P<check>is|is not) a (?P<expected_type>array|dictionary)')
def step_check_data(context, name, key, check, expected_type):
    """Check key are present and the value is list or dict"""
    type_checker = dict if expected_type == "dictionary" else list
    for val in context.vars['body']:
        if name in val['data']:
            assert_that(val['data'][name], has_key(key))
            if check == "is":
                assert_that(val['data'][name][key], instance_of(type_checker))
            else:
                assert_that(val['data'][name][key], is_not(instance_of(type_checker)))
