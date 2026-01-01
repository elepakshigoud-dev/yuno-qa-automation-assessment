Feature: Verify Payment

  @Regression @Integration
  Scenario: Verify payment using verify flag
    Given payment request with verify true
    When user sends verify payment request
    Then verification should be successful

  @Negative
  Scenario: Verify payment fails for invalid request
    Given invalid verify payment request
    When user sends verify payment request
    Then error response should be returned
