from behave import given, when
from facts.webhook import WebhookFacts
from tasks.webhook import WebhookTask


@given("a requestbin user creates a bin with the key '{key}'")
def step_impl(context, key):
    status, header, body = WebhookFacts.create_bin(key)
    context.status = status
    context.body = body


@when("receive a webook with '{key}' as key")
def step_impl(context, key):
    status, header, body = WebhookTask.get_bin(key)
    context.status = status
    context.expected_body = body
