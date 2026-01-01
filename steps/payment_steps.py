from behave import given, when, then

@given('valid purchase request with minimal fields')
def step_valid_purchase(context):
    pass

@when('user sends purchase payment request')
def step_send_purchase(context):
    pass

@then('payment should be successful')
def step_purchase_success(context):
    pass

@given('purchase request with invalid card')
def step_invalid_card(context):
    pass

@then('error response should be returned')
def step_error_response(context):
    pass


@given('valid refund request')
def step_valid_refund(context):
    pass

@when('user sends refund request')
def step_send_refund(context):
    pass

@then('refund should be successful')
def step_refund_success(context):
    pass


@given('authorization request with minimal fields')
def step_auth_request(context):
    pass

@when('user sends authorization request')
def step_send_auth(context):
    pass

@then('authorization should be successful')
def step_auth_success(context):
    pass


@given('payment request with verify true')
def step_verify_request(context):
    pass

@when('user sends verify payment request')
def step_send_verify(context):
    pass

@then('verification should be successful')
def step_verify_success(context):
    pass
