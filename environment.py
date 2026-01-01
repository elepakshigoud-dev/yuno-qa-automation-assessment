
import yaml
from pathlib import Path

def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / "config" / "config.yaml"
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            print(f"✅ Configuration loaded successfully")
            return config
    except FileNotFoundError:
        print(f"❌ Error: config.yaml not found at {config_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"❌ Error parsing config.yaml: {e}")
        return {}

def before_all(context):
    """Run before all features"""
    print("=" * 50)
    print("🚀 Starting Yuno Payment API Test Suite")
    print("=" * 50)
    
    # Load configuration
    context.config = load_config()
    
    if context.config:
        # Store config in context for easy access
        context.base_url = context.config.get('api', {}).get('base_url', '')
        context.account_id = context.config.get('api', {}).get('account_id', '')
        context.test_cards = context.config.get('test_cards', {})
        
        print(f"📡 API Base URL: {context.base_url}")
        print(f"👤 Account ID: {context.account_id}")
    else:
        print("⚠️  Warning: No configuration loaded")

def before_scenario(context, scenario):
    """Run before each scenario"""
    print(f"\n📋 Scenario: {scenario.name}")
    
    # Initialize scenario-specific variables
    context.payment_id = None
    context.authorization_id = None
    context.customer_id = None
    context.refund_id = None
    context.response = None
    context.error_message = None
    
    # Ensure workflow is DIRECT as per requirements
    context.workflow = "DIRECT"

def after_scenario(context, scenario):
    """Run after each scenario"""
    if scenario.status == "passed":
        print(f"✅ {scenario.name} - PASSED")
    else:
        print(f"❌ {scenario.name} - FAILED")
    
    # Cleanup
    if hasattr(context, 'response'):
        del context.response

def after_all(context):
    """Run after all features"""
    print("\n" + "=" * 50)
    print("🏁 Test Suite Execution Completed")
    print("=" * 50)
