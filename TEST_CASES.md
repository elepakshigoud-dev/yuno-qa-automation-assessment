# Yuno Payment API - Test Cases Documentation

## 📋 Overview
This document outlines test scenarios for Yuno Payment API automation suite.

---

## 🧪 Test Suite Classification

### **1. Sanity Suite** (Critical Path)
| Test Case | Description                                 | Priority |
|-----------|---------------------------------------------|----------|
| TC-001    | Create payment with minimal required fields   | P0 |
| TC-002    | Create payment with valid card details        | P0 |
| TC-003    | Verify payment method                         | P0 |
| TC-004    | Create customer with basic details            | P0 |

### **2. Regression Suite** (All Functionalities)
| Test Case | Description                       m     | Priority |
|-----------|-----------------------------------------|----------|
| TC-101    | Create payment with customer_payer data    | P1 |
| TC-102    | Create payment with additional_data        | P1 |
| TC-103    | Full refund of successful payment          | P1 |
| TC-104    | Partial refund of successful payment       | P1 |
| TC-105    | Create authorization with minimal fields   | P1 |
| TC-106    | Create authorization with customer_payer   | P1 |
| TC-107    | Capture full authorization amount          | P1 |
| TC-108    | Capture partial authorization amount       | P1 |
| TC-109    | Cancel payment before capture              | P1 |
| TC-110    | Create and verify customer                 | P1 |
| TC-111    | Enroll payment method for customer         | P1 |

### **3. Integration Suite** (End-to-End Flows)
| Test Case | Description                                         | Priority |
------------------------------------------------------------------------------
| TC-201    | Complete purchase → refund flow                       | P2 |
| TC-202    | Authorization → capture → refund flow                 | P2 |
| TC-203    | Customer creation → payment enrollment → payment flow | P2 |
| TC-204    | Verify → purchase flow                                | P2 |
  
---

## 🔴 Negative Test Scenarios

### **Payment Creation Negative Tests**
| Test Case | Description                      | Expected Result         |
|-----------|----------------------------------|-------------------------|
| TC-N001   | Missing required field (amount)  | 400 Bad Request         |
| TC-N002   | Invalid currency code            | 400 Bad Request         |
| TC-N003   | Invalid card number (declined)   | Payment declined        |
| TC-N004   | Expired card date                | Card expired error      |
| TC-N005   | Invalid CVV code                 | CVV validation error    |
| TC-N006   | Missing workflow=DIRECT          | 400 Bad Request         |
| TC-N007   | Duplicate idempotency key        | Idempotency error       |
| TC-N008   | Amount = 0                       | Amount validation error |
| TC-N009   | Amount = negative value          | Amount validation error |
| TC-N010   | Exceed maximum amount limit      | Amount limit exceeded   |

### **Refund Negative Tests**
| Test Case | Description                     | Expected Result         |
|-----------|---------------------------------|-------------------------|
| TC-N101   | Refund non-existent payment     | Payment not found       |
| TC-N102   | Refund already refunded payment | Already refunded error  |
| TC-N103   | Refund amount > original amount | Exceeds amount error    |
| TC-N104   | Refund cancelled payment        | Invalid payment state   |

### **Authorization Negative Tests**
| Test Case | Description                            | Expected Result           |
|-----------|----------------------------------------|---------------------------|
| TC-N201   | Capture before authorization           | Authorization not found   |
| TC-N202   | Capture amount > authorized amount     | Exceeds authorized amount |
| TC-N203   | Cancel already captured authorization  | Invalid state error       |
| TC-N204   | Capture already captured authorization | Already captured error    |

### **Customer Negative Tests**
| Test Case | Description                        | Expected Result        |
|-----------|------------------------------------|------------------------|
| TC-N301   | Create customer with invalid email | Email validation error |
| TC-N302   | Duplicate customer email           | Customer exists error  |
| TC-N303   | Enroll invalid payment method      | Payment method invalid |

---

## 📊 Functional Requirements

### **Payment Flow Requirements**
1. **FR-001**: API must accept payment creation with valid credentials
2. **FR-002**: All payments must include `workflow: "DIRECT"`
3. **FR-003**: Idempotency key must prevent duplicate transactions
4. **FR-004**: Payment status must be accurately reflected (SUCCESS/FAILED)
5. **FR-005**: Error messages must be clear and actionable

### **Refund Flow Requirements**
1. **FR-101**: Support both full and partial refunds
2. **FR-102**: Refund must reference original payment ID
3. **FR-103**: Refund status must be trackable

### **Authorization Flow Requirements**
1. **FR-201**: Authorization must reserve funds without capture
2. **FR-202**: Support partial and full capture
3. **FR-203**: Authorization expiry must be enforced

### **Customer Management Requirements**
1. **FR-301**: Customer creation with unique identifier
2. **FR-302**: Payment method enrollment for customers
3. **FR-303**: Customer data privacy and security

---

## ⚡ Non-Functional Requirements

### **Performance Requirements**
1. **NFR-001**: API response time < 2 seconds for all endpoints
2. **NFR-002**: Payment processing time < 5 seconds
3. **NFR-003**: Support 100+ concurrent transactions

### **Security Requirements**
1. **NFR-101**: All requests must be authenticated with API keys
2. **NFR-102**: Sensitive data (card details) must be encrypted
3. **NFR-103**: Idempotency must be guaranteed
4. **NFR-104**: Rate limiting must be implemented

### **Reliability Requirements**
1. **NFR-201**: API availability 99.9% uptime
2. **NFR-202**: Error rate < 0.1%
3. **NFR-203**: Data consistency across all operations

### **Usability Requirements**
1. **NFR-301**: Clear and consistent error messages
2. **NFR-302**: Comprehensive API documentation
3. **NFR-303**: Transaction status tracking

---

## 🏷️ Test Tags Mapping

### **Behave Tags for Test Execution**
```gherkin
@sanity      - Critical path tests (TC-001 to TC-004)
@regression  - All functional tests (TC-101 to TC-111)
@integration - End-to-end flows (TC-201 to TC-204)
@negative    - Negative test scenarios (TC-N001 to TC-N303)
@payment     - Payment related tests
@refund      - Refund related tests
@authorization - Authorization flow tests
@customer    - Customer management tests
