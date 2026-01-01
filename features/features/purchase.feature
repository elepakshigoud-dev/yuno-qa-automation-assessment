Feature: Purchase Payment

  @Sanity @Integration
  Scenario: Successful purchase with minimal fields
    Given valid purchase request with minimal fields
    When user sends purchase payment request
    Then payment should be successful

  @Regression @Negative
  Scenario: Purchase fails with invalid card number
    Given purchase request with invalid card
    When user sends purchase payment request
    Then error response should be returned
