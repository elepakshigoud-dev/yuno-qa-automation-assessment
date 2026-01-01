Feature: Authorization Payment

  @Sanity
  Scenario: Authorization with minimal fields
    Given authorization request with minimal fields
    When user sends authorization request
    Then authorization should be successful

  @Regression
  Scenario: Capture authorized payment
    Given authorized payment exists
    When user captures the payment
    Then capture should be successful
