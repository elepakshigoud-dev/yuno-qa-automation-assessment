Feature: Refund Payment

  @Regression @Integration
  Scenario: Successful refund
    Given valid refund request
    When user sends refund request
    Then refund should be successful

  @Negative
  Scenario: Refund fails for invalid payment id
    Given refund request with invalid payment id
    When user sends refund request
    Then error response should be returned
