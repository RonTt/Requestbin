from behave import then
from questions.status import StatusQuestions

@then("the request succeeded")
def step_impl(context):    
    assert(StatusQuestions.is_ok(context.status))
