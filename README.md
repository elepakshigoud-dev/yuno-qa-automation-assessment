# Yuno QA Automation Assessment

## Tech Stack
- Python
- Behave (BDD Framework)
- Requests Library

## Project Structure
- Features written in Gherkin language
- Step definitions implemented in Python
- Covers Purchase, Refund, Authorization, Capture and Verify workflows

## Test Coverage
### Functional Scenarios
- Purchase with minimal and maximal fields
- Authorization and Capture
- Refund and Cancel flows
- Verify payment flow

### Negative Scenarios
- Invalid card numbers
- Missing mandatory fields
- Invalid payment id
- Duplicate idempotency key

## Test Classification
- Sanity: Critical purchase and authorization flows
- Regression: End-to-end payment flows
- Integration: API level validations

## Functional Requirements
- System should create payments using DIRECT workflow
- System should support refunds and cancellations
- System should validate payment and card details

## Non-Functional Requirements
- Security of API keys
- Reliability of payment processing
- Idempotency handling for duplicate requests

## Execution Steps
1. Install dependencies:
   pip install -r requirements.txt
2. Run tests:
   behave
