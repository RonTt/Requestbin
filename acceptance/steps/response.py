from behave import then

@then("the response body is as expected")
def step_impl(context):
    assert context.body == context.expected_body


