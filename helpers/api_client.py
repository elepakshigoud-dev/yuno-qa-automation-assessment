# helpers/api_client.py
"""
Yuno API Client for payment operations
Handles all API calls with proper authentication and error handling
"""

import requests
import uuid
import json
import logging
from typing import Optional, Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YunoAPIClient:
    """Client for interacting with Yuno Payment API"""
    
    def __init__(self, base_url: str, public_key: str, private_key: str, account_id: str):
        """
        Initialize API client
        
        Args:
            base_url: Base URL for API (e.g., "https://api.y.uno/v1")
            public_key: Public API key
            private_key: Private secret key
            account_id: Merchant account ID
        """
        self.base_url = base_url.rstrip('/')
        self.public_key = public_key
        self.private_key = private_key
        self.account_id = account_id
        
        logger.info(f"Initialized YunoAPIClient for account: {account_id}")
    
    def _generate_idempotency_key(self) -> str:
        """Generate a unique idempotency key for each request"""
        return str(uuid.uuid4())
    
    def _get_headers(self, custom_headers: Optional[Dict] = None) -> Dict[str, str]:
        """
        Generate standard headers for API requests
        
        Returns:
            Dictionary of headers including authentication and idempotency
        """
        headers = {
            "public-api-key": self.public_key,
            "private-secret-key": self.private_key,
            "x-idempotency-key": self._generate_idempotency_key(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    def _make_request(self, method: str, endpoint: str, 
                     payload: Optional[Dict] = None, 
                     expected_status: int = 200) -> Dict[str, Any]:
        """
        Make HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., "/payments")
            payload: Request payload
            expected_status: Expected HTTP status code
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.exceptions.RequestException: If request fails
            AssertionError: If response status doesn't match expected
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        # Log request details
        logger.info(f"Making {method} request to: {url}")
        if payload:
            logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # Log response details
            logger.info(f"Response Status: {response.status_code}")
            
            # Parse JSON response
            response_data = {}
            if response.text:
                try:
                    response_data = response.json()
                    logger.debug(f"Response: {json.dumps(response_data, indent=2)}")
                except json.JSONDecodeError:
                    logger.warning(f"Non-JSON response: {response.text}")
                    response_data = {"raw_response": response.text}
            
            # Validate response status
            if response.status_code != expected_status:
                logger.error(f"Unexpected status: {response.status_code}. Expected: {expected_status}")
                logger.error(f"Response: {response_data}")
            
            # Add status code to response data
            response_data['_status_code'] = response.status_code
            response_data['_headers'] = dict(response.headers)
            
            return response_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    # ==================== PAYMENT OPERATIONS ====================
    
    def create_payment(self, amount: float, currency: str, 
                      payment_method: Dict, 
                      customer_payer: Optional[Dict] = None,
                      additional_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a payment
        
        Args:
            amount: Payment amount
            currency: Currency code (e.g., "USD")
            payment_method: Payment method details
            customer_payer: Customer information (optional)
            additional_data: Additional payment data (optional)
            
        Returns:
            Payment creation response
        """
        payload = {
            "account_id": self.account_id,
            "amount": amount,
            "currency": currency,
            "workflow": "DIRECT",
            "payment_method": payment_method
        }
        
        if customer_payer:
            payload["customer_payer"] = customer_payer
        
        if additional_data:
            payload["additional_data"] = additional_data
        
        return self._make_request("POST", "/payments", payload)
    
    def refund_payment(self, payment_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """
        Refund a payment
        
        Args:
            payment_id: ID of payment to refund
            amount: Amount to refund (partial refund). If None, full refund.
            
        Returns:
            Refund response
        """
        payload = {"payment_id": payment_id}
        if amount is not None:
            payload["amount"] = amount
        
        return self._make_request("POST", "/refunds", payload)
    
    # ==================== AUTHORIZATION OPERATIONS ====================
    
    def create_authorization(self, amount: float, currency: str,
                           payment_method: Dict,
                           customer_payer: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create an authorization
        
        Args:
            amount: Authorization amount
            currency: Currency code
            payment_method: Payment method details
            customer_payer: Customer information (optional)
            
        Returns:
            Authorization response
        """
        payload = {
            "account_id": self.account_id,
            "amount": amount,
            "currency": currency,
            "workflow": "DIRECT",
            "payment_method": payment_method
        }
        
        if customer_payer:
            payload["customer_payer"] = customer_payer
        
        return self._make_request("POST", "/authorizations", payload)
    
    def capture_authorization(self, authorization_id: str, 
                            amount: Optional[float] = None) -> Dict[str, Any]:
        """
        Capture an authorization
        
        Args:
            authorization_id: Authorization ID to capture
            amount: Amount to capture (partial capture). If None, full capture.
            
        Returns:
            Capture response
        """
        payload = {"authorization_id": authorization_id}
        if amount is not None:
            payload["amount"] = amount
        
        return self._make_request("POST", "/captures", payload)
    
    def cancel_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Cancel a payment
        
        Args:
            payment_id: Payment ID to cancel
            
        Returns:
            Cancel response
        """
        payload = {"payment_id": payment_id}
        return self._make_request("POST", "/cancels", payload)
    
    # ==================== VERIFICATION ====================
    
    def verify_payment(self, payment_method: Dict) -> Dict[str, Any]:
        """
        Verify a payment method
        
        Args:
            payment_method: Payment method details
            
        Returns:
            Verification response
        """
        payload = {
            "account_id": self.account_id,
            "amount": 1,  # Minimal amount for verification
            "currency": "USD",
            "workflow": "DIRECT",
            "payment_method": payment_method,
            "verify": True
        }
        
        return self._make_request("POST", "/payments", payload)
    
    # ==================== CUSTOMER OPERATIONS ====================
    
    def create_customer(self, email: str, name: str, 
                       additional_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a customer
        
        Args:
            email: Customer email
            name: Customer name
            additional_data: Additional customer data (optional)
            
        Returns:
            Customer creation response
        """
        payload = {
            "account_id": self.account_id,
            "email": email,
            "name": name
        }
        
        if additional_data:
            payload.update(additional_data)
        
        return self._make_request("POST", "/customers", payload)
    
    def enroll_payment_method(self, customer_id: str, 
                            payment_method: Dict) -> Dict[str, Any]:
        """
        Enroll a payment method for customer
        
        Args:
            customer_id: Customer ID
            payment_method: Payment method details
            
        Returns:
            Enrollment response
        """
        payload = {
            "account_id": self.account_id,
            "customer_id": customer_id,
            "payment_method": payment_method
        }
        
        return self._make_request("POST", "/payment-methods/enroll", payload)
    
    # ==================== GET OPERATIONS ====================
    
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment status
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Payment status response
        """
        return self._make_request("GET", f"/payments/{payment_id}")
    
    def get_refund_status(self, refund_id: str) -> Dict[str, Any]:
        """
        Get refund status
        
        Args:
            refund_id: Refund ID
            
        Returns:
            Refund status response
        """
        return self._make_request("GET", f"/refunds/{refund_id}")
    
    # ==================== TEST DATA GENERATORS ====================
    
    @staticmethod
    def generate_test_card(success: bool = True) -> Dict[str, str]:
        """
        Generate test card data
        
        Args:
            success: If True, returns valid card. If False, returns invalid card.
            
        Returns:
            Card data dictionary
        """
        if success:
            return {
                "type": "CARD",
                "card": {
                    "number": "4111111111111111",
                    "expiration_month": "12",
                    "expiration_year": "2025",
                    "holder_name": "TEST USER",
                    "cvv": "123"
                }
            }
        else:
            return {
                "type": "CARD",
                "card": {
                    "number": "4000000000000002",  # Test decline card
                    "expiration_month": "12",
                    "expiration_year": "2025",
                    "holder_name": "TEST USER",
                    "cvv": "123"
                }
            }
    
    @staticmethod
    def generate_customer_data() -> Dict[str, str]:
        """
        Generate test customer data
        
        Returns:
            Customer data dictionary
        """
        import random
        customer_id = random.randint(10000, 99999)
        return {
            "email": f"test.customer{customer_id}@example.com",
            "name": f"Test Customer {customer_id}",
            "document": f"DOC{customer_id}",
            "document_type": "ID"
        }
