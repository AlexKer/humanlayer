"""
Simple Baseten + HumanLayer Demo

Perfect for Instagram reels - shows AI agent making increasingly questionable decisions
that get caught by human oversight.
"""

import os
from humanlayer import HumanLayer

# Initialize HumanLayer
hl = HumanLayer(
    api_key=os.getenv("HUMANLAYER_API_KEY"),
    verbose=True
)

# Mock purchase function that requires approval for expensive items
@hl.require_approval()
def make_company_purchase(item: str, cost: float, justification: str):
    """Make a company purchase - requires approval for financial safety"""
    return f"💳 Purchased {item} for ${cost:,.2f} - {justification}"

def instagram_reel_demo():
    """Perfect for social media demo"""
    
    print("🤖 AI Assistant: Starting office supply run...\n")
    
    # The agent's increasingly questionable decisions
    purchases = [
        ("Office chairs", 150, "Basic seating upgrade"),
        ("Coffee machine", 800, "Team productivity boost"), 
        ("Gaming setup", 3500, "Enhanced developer experience"),
        ("Tesla Model S", 89000, "Company vehicle for client meetings"),
        ("Private jet", 2000000, "Faster travel to meetings")
    ]
    
    for item, cost, justification in purchases:
        print(f"🛒 Attempting to buy: {item} (${cost:,})")
        
        if cost > 100:  # Trigger approval for "expensive" items
            print("   ⏳ APPROVAL NEEDED - Notification sent to your phone...")
            # In real usage, this would trigger HumanLayer approval
            # result = make_company_purchase(item, cost, justification)
            print(f"   📱 Human review required for ${cost:,} purchase")
        else:
            print(f"   ✅ Approved automatically - ${cost}")
        
        print()
    
    print("✅ Crisis averted by HumanLayer!")
    print("💡 AI agents need human oversight for high-stakes decisions")

if __name__ == "__main__":
    # Check if environment is set up
    if not os.getenv("HUMANLAYER_API_KEY"):
        print("⚠️  Set HUMANLAYER_API_KEY to see full approval flow")
        print("For now, showing mock demo...\n")
    
    instagram_reel_demo()
